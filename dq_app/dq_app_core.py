import great_expectations as gx
from dq_app import dataset as ds
from dq_app import dq_expectation as de
from dq_app import dq_rule as dr

import json

from dq_app import settings as sc

import logging

from utils import file_io as uff


def get_expectation_by_id(exp_id: str) -> de.DQExpectation:
    dq_expectations_json_file = f"{sc.api_data_path}/{sc.api_dq_expectations_file}"
    dq_expectation = de.DQExpectation.from_json(
        dq_expectations_json_file, "dq_expectations", exp_id
    )

    # print(dq_expectation)
    return dq_expectation


def get_dq_rules_by_dataset_id(
    dataset_id: str, dq_rules: list[dr.DQRule]
) -> list[dr.DQRule]:
    dq_rules_for_dataset = []

    for dq_rule in dq_rules:
        if dataset_id == dq_rule.dataset_id:
            dq_rules_for_dataset.append(dq_rule)

    # print(dq_rules_for_dataset)
    return dq_rules_for_dataset


def get_all_dq_rules_from_json(json_file: str, json_key: str) -> list[dr.DQRule]:
    # with open(json_file, 'r') as f:
    with uff.uf_open_file(file_path=json_file, open_mode="r") as f:
        dq_rules: list[dict] = json.load(f)[json_key]

    try:
        if dq_rules:
            # print(dq_rules)
            dq_rule_objects = []
            for dq_rule in dq_rules:
                dq_rule_objects.append(dr.DQRule(**dq_rule))
            return dq_rule_objects
        else:
            raise ValueError("DQ rules data is invalid.")
    except ValueError as error:
        logging.error(error)
        raise


def apply_dq_rules(dataset_id) -> list:

    # Simulate getting the dataset metadata from API
    datasets_json_file = f"{sc.api_data_path}/{sc.api_datasets_file}"
    dataset = ds.LocalDelimFileDataset.from_json(
        datasets_json_file, "datasets", dataset_id
    )

    # Simulate getting all DQ rules from API
    dq_rules_json_file = f"{sc.api_data_path}/{sc.api_dq_rules_file}"
    dq_rules = get_all_dq_rules_from_json(dq_rules_json_file, "dq_rules")

    # Get DQ rules defined for the dataset
    dq_rules_for_dataset = get_dq_rules_by_dataset_id(dataset.dataset_id, dq_rules)

    # Define the GE context
    context = gx.get_context()

    # Use the `pandas_default` Data Source to retrieve a Batch of sample Data from a data file:
    src_file_path = sc.resolve_app_path(dataset.file_path)
    batch = context.data_sources.pandas_default.read_csv(src_file_path)

    # Apply the DQ rules on the dataset
    dq_check_results = []
    for dq_rule in dq_rules_for_dataset:
        dq_expectation = get_expectation_by_id(dq_rule.exp_id)

        # Assign the GE function name to a string
        gen_func_str = f"gen_func = gx.expectations.{dq_expectation.exp_name}"
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
                rule_id=dq_rule.rule_id, dq_check_output=validation_results
            )
            dq_check_results.append(dq_check_result)

    return dq_check_results


def fmt_dq_check_result(rule_id, dq_check_output) -> dict:
    dq_check_status = dq_check_output["success"]

    if dq_check_status:
        dq_check_result = {"rule_id": rule_id, "result": dq_check_status}
    else:
        dq_check_result = {"rule_id": rule_id, "result": False}

    return dq_check_result
