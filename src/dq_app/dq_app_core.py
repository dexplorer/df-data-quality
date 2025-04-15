import great_expectations as gx
import importlib
from metadata import dataset as ds
from metadata import data_source as dsrc
from metadata import dq_expectation as de
from metadata import dataset_dq_rule as dr
from app_calendar import eff_date as ed
from config.settings import ConfigParms as sc

from pyspark.sql import SparkSession, DataFrame
from utils import spark_io as ufs
from utils import aws_s3_io as ufas
import os
import logging


def apply_dq_rules(dataset_id: str, cycle_date: str) -> list:
    # Simulate getting the cycle date from API
    # Run this from the parent app
    if not cycle_date:
        cycle_date = ed.get_cur_cycle_date()

    # Simulate getting the dataset metadata from API
    logging.info("Get dataset metadata")
    # dataset = ds.LocalDelimFileDataset.from_json(dataset_id)
    dataset = ds.get_dataset_from_json(dataset_id=dataset_id)

    # Simulate getting the data source metadata from API
    data_source = dsrc.get_data_source_from_json(data_source_id=dataset.data_source_id)

    # Simulate getting all DQ rules from API
    logging.info("Get all DQ rules")
    dq_rules = dr.get_all_dq_rules_from_json()

    # Get DQ rules defined for the dataset
    logging.info("Get all DQ rules associated with the dataset")
    dq_rules_for_dataset = dr.get_dq_rules_by_dataset_id(dataset.dataset_id, dq_rules)

    # Get current effective date
    cur_eff_date = ed.get_cur_eff_date(
        schedule_id=dataset.schedule_id, cycle_date=cycle_date
    )
    cur_eff_date_yyyymmdd = ed.fmt_date_str_as_yyyymmdd(cur_eff_date)

    ge_context = create_ge_context()
    ge_data_source = create_spark_data_source(
        ge_context=ge_context, ge_data_source_name="spark local"
    )
    ge_data_asset = create_data_asset(
        ge_data_source=ge_data_source, ge_data_asset_name="spark data"
    )
    ge_batch_definition = add_batch_definition(
        ge_data_asset=ge_data_asset, ge_batch_definition_name="spark batch"
    )
    spark: SparkSession = ufs.create_spark_session(
        warehouse_path=sc.hive_warehouse_path
    )
    src_df = ufs.create_empty_df(spark=spark)
    if dataset.dataset_type == ds.DatasetType.LOCAL_DELIM_FILE:
        # Read the source data file
        src_file_path = sc.resolve_app_path(
            dataset.resolve_file_path(
                date_str=cur_eff_date_yyyymmdd,
                data_source_user=data_source.data_source_user,
            )
        )

        if os.path.exists(src_file_path):
            logging.info("Reading the file %s", src_file_path)
            src_df = ufs.read_delim_file_into_spark_df(
                file_path=src_file_path,
                delim=dataset.file_delim,
                spark=spark,
            )

        else:
            logging.info("File %s does not exist. Skipping the file.", src_file_path)

    elif dataset.dataset_type == ds.DatasetType.SPARK_TABLE:
        # Read the spark table
        qual_table_name = dataset.get_qualified_table_name()
        logging.info("Reading the spark table %s", qual_table_name)
        src_df = ufs.read_spark_table_into_spark_df(
            qual_table_name=qual_table_name,
            cur_eff_date=cur_eff_date,
            spark=spark,
        )

    elif dataset.dataset_type == ds.DatasetType.AWS_S3_DELIM_FILE:
        s3_client = ufas.get_s3_client(s3_region=sc.s3_region)

        # Read the source data file
        src_file_uri = sc.resolve_app_path(
            dataset.resolve_file_uri(
                date_str=cur_eff_date_yyyymmdd,
                data_source_user=data_source.data_source_user,
            )
        )

        if ufas.s3_obj_exists(s3_obj_uri=src_file_uri, s3_client=s3_client):
            logging.info("Reading the file %s", src_file_uri)
            src_df = ufs.read_delim_file_into_spark_df(
                file_path=src_file_uri.replace("s3://", "s3a://"),
                # file_path=src_file_uri,
                delim=dataset.file_delim,
                spark=spark,
            )
        else:
            logging.info("File %s does not exist. Skipping the file.", src_file_uri)

    batch_parameters = define_batch_parms_for_spark_df(df=src_df)
    batch = ge_batch_definition.get_batch(batch_parameters=batch_parameters)

    # Apply the DQ rules on the dataset
    logging.info("Apply DQ rules on the dataset")
    dq_check_results = []
    for dq_rule in dq_rules_for_dataset:
        dq_expectation = de.DQExpectation.from_json(exp_id=dq_rule.exp_id)

        # Assign the GE function name to a string
        mod_name = "great_expectations.expectations"
        func_name = dq_expectation.ge_method
        mod = importlib.import_module(mod_name)
        # Get the function defined in the DQ batch object
        gen_func = getattr(mod, func_name)
        # Pass the keyword arguments to the function
        expectation = gen_func(**dq_rule.kwargs)

        # Assign the GE function name to a string
        # gen_func_str = f"gen_func = gx.expectations.{dq_expectation.ge_method}"
        # Get local variables
        # _locals = locals()
        # Execute the function name assignment, this mutates the local namespace
        # exec(gen_func_str, globals(), _locals)
        # Grab the newly defined function name from the local namespace dictionary and assign it to generic function variable
        # gen_func = _locals["gen_func"]
        # Pass function specific keyword arguments to the generic function
        # expectation = gen_func(**dq_rule.kwargs)

        if expectation:
            # Run the validation
            validation_results = batch.validate(expectation)

            dq_check_result = fmt_dq_check_result(
                rule_id=dq_rule.rule_id,
                exp_name=dq_expectation.exp_name,
                dq_check_output=validation_results,
            )
            dq_check_results.append(dq_check_result)

    return dq_check_results


def create_ge_context():
    # Define the GE context
    ge_context = gx.get_context(mode="ephemeral")
    return ge_context


def create_spark_data_source(ge_context, ge_data_source_name: str):
    ge_data_source = ge_context.data_sources.add_spark(name=ge_data_source_name)
    return ge_data_source


def create_data_asset(ge_data_source, ge_data_asset_name: str):
    ge_data_asset = ge_data_source.add_dataframe_asset(name=ge_data_asset_name)
    return ge_data_asset


def add_batch_definition(ge_data_asset, ge_batch_definition_name: str):
    ge_batch_definition = ge_data_asset.add_batch_definition_whole_dataframe(
        name=ge_batch_definition_name
    )
    return ge_batch_definition


def define_batch_parms_for_spark_df(df: DataFrame):
    ge_batch_parameters = {"dataframe": df}
    return ge_batch_parameters


def fmt_dq_check_result(rule_id: str, exp_name: str, dq_check_output: dict) -> dict:
    if dq_check_output["success"]:
        dq_check_status = "Pass"
    else:
        dq_check_status = "Fail"

    dq_check_result = {
        "rule_id": rule_id,
        "result": dq_check_status,
        "expectation": exp_name,
    }

    return dq_check_result
