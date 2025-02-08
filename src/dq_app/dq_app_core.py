import great_expectations as gx
from metadata import dataset as ds
from metadata import dq_expectation as de
from metadata import dq_rule as dr
from app_calendar import eff_date as ed
from dq_app.settings import ConfigParms as sc

import logging


def apply_dq_rules(dataset_id: str, cycle_date: str) -> list:

    # Simulate getting the dataset metadata from API
    logging.info("Get dataset metadata")
    # dataset = ds.LocalDelimFileDataset.from_json(dataset_id)
    dataset = ds.get_dataset_from_json(dataset_id=dataset_id)

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

    # Define the GE context
    context = gx.get_context()

    # Read the source data file
    src_file_path = sc.resolve_app_path(
        dataset.resolve_file_path(cur_eff_date_yyyymmdd)
    )
    batch = context.data_sources.pandas_default.read_csv(src_file_path)

    # Apply the DQ rules on the dataset
    logging.info("Apply DQ rules on the dataset")
    dq_check_results = []
    for dq_rule in dq_rules_for_dataset:
        dq_expectation = de.DQExpectation.from_json(exp_id=dq_rule.exp_id)

        # Assign the GE function name to a string
        gen_func_str = f"gen_func = gx.expectations.{dq_expectation.ge_method}"
        # Get local variables
        _locals = locals()
        # Execute the function name assignment, this mutates the local namespace
        exec(gen_func_str, globals(), _locals)
        # Grab the newly defined function name from the local namespace dictionary and assign it to generic function variable
        gen_func = _locals["gen_func"]
        # Pass function specific keyword arguments to the generic function
        expectation = gen_func(**dq_rule.kwargs)

        if expectation:
            # Test the Expectation:
            validation_results = batch.validate(expectation)

            # Evaluate the Validation Results:
            # print(validation_results)

            dq_check_result = fmt_dq_check_result(
                rule_id=dq_rule.rule_id,
                exp_name=dq_expectation.exp_name,
                dq_check_output=validation_results,
            )
            dq_check_results.append(dq_check_result)

    return dq_check_results


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
