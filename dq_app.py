import great_expectations as gx
from dataset import LocalDelimFileDataset
from dq_expectation import DQExpectation
from dq_rule import DQRule


def get_expectation_by_id(exp_id, dq_expectations):
    for dq_expectation in dq_expectations:
        if exp_id == dq_expectation.exp_id:
            return dq_expectation
    return None


def apply_dq_rules(batch, dq_rules, dq_expectations) -> list:
    dq_check_results = []

    for dq_rule in dq_rules:
        dq_expectation = get_expectation_by_id(dq_rule.exp_id, dq_expectations)

        if dq_expectation.exp_name == "ExpectColumnValuesToBeUnique":
            # Define the Expectation to test:
            expectation = gx.expectations.ExpectColumnValuesToBeUnique(
                column=dq_rule.column_name
            )

        elif dq_expectation.exp_name == "ExpectColumnValuesToBeInSet":
            expectation = gx.expectations.ExpectColumnValuesToBeInSet(
                column=dq_rule.column_name, value_set=["equity", "mutual fund"]
            )

        elif dq_expectation.exp_name == "ExpectColumnValuesToBeBetween":
            expectation = gx.expectations.ExpectColumnValuesToBeBetween(
                column=dq_rule.column_name, min_value=5, max_value=50
            )

        else:
            expectation = None

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


def main():
    dq_expectations = [
        DQExpectation(
            exp_id="1",
            exp_name="ExpectColumnValuesToBeUnique",
            ge_method="ExpectColumnValuesToBeUnique",
        ),
        DQExpectation(
            exp_id="2",
            exp_name="ExpectColumnValuesToBeInSet",
            ge_method="ExpectColumnValuesToBeInSet",
        ),
        DQExpectation(
            exp_id="3",
            exp_name="ExpectColumnValuesToBeBetween",
            ge_method="ExpectColumnValuesToBeBetween",
        ),
    ]

    dq_rules = [
        DQRule(
            rule_id="1",
            dataset_id="1",
            column_name="asset_id",
            exp_id="1",
            rule_fail_action="abort",
        ),
        DQRule(
            rule_id="2",
            dataset_id="1",
            column_name="asset_type",
            exp_id="2",
            rule_fail_action="abort",
        ),
        DQRule(
            rule_id="3",
            dataset_id="1",
            column_name="asset_id",
            exp_id="3",
            rule_fail_action="proceed",
        ),
    ]

    dataset = LocalDelimFileDataset(
        dataset_id="1",
        cataloged_ind=True,
        file_delim=",",
        file_path="./data/test_data.csv",
    )
    # dataset.add_dq_rule()

    # Define the context
    context = gx.get_context()

    # Use the `pandas_default` Data Source to retrieve a Batch of sample Data from a data file:
    batch = context.data_sources.pandas_default.read_csv(dataset.file_path)

    dq_check_results = apply_dq_rules(batch, dq_rules, dq_expectations)

    if dq_check_results:
        for dq_check_result in dq_check_results:
            print(
                f"Rule Id: {dq_check_result['rule_id']} Result: {dq_check_result['result']}"
            )
    else:
        print("DQ check rules are not applied successfully.")


if __name__ == "__main__":
    main()
