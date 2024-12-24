import great_expectations as gx 


def apply_dq_rules(batch, dq_rules_cnt) -> list:
    dq_check_results = []

    # Define the Expectation to test:
    expectation = gx.expectations.ExpectColumnValuesToBeUnique(column='asset_id')

    # Test the Expectation:
    validation_results = batch.validate(expectation)

    # Evaluate the Validation Results:
    # print(validation_results)

    dq_check_result = fmt_dq_check_result(rule_id='1', dq_check_output=validation_results)
    dq_check_results.append(dq_check_result)

    expectation = gx.expectations.ExpectColumnValuesToBeInSet(column='asset_type', value_set=['equity', 'mutual fund'])
    validation_results = batch.validate(expectation)
    dq_check_result = fmt_dq_check_result(rule_id='2', dq_check_output=validation_results)
    dq_check_results.append(dq_check_result)

    expectation = gx.expectations.ExpectColumnValuesToBeBetween(column='asset_id', min_value=5, max_value=50)
    validation_results = batch.validate(expectation)
    dq_check_result = fmt_dq_check_result(rule_id='3', dq_check_output=validation_results)
    dq_check_results.append(dq_check_result)

    return dq_check_results

def fmt_dq_check_result(rule_id, dq_check_output) -> dict:
    dq_check_status = dq_check_output['success']

    if dq_check_status:
        dq_check_result = {
            'rule_id': rule_id, 
            'result': dq_check_status
        }
    else: 
        dq_check_result = {
            'rule_id': rule_id, 
            'result': False
        }

    return dq_check_result

def main():
    # This example uses a File Data Context which already has
    #  a Data Source defined.
    context = gx.get_context()

    # Use the `pandas_default` Data Source to retrieve a Batch of sample Data from a data file:
    file_path = "./data/test_data.csv"
    batch = context.data_sources.pandas_default.read_csv(file_path)

    dq_check_results = apply_dq_rules(batch, 2)

    if dq_check_results:
        for dq_check_result in dq_check_results:
            print(f"Rule Id: {dq_check_result['rule_id']} Result: {dq_check_result['result']}")
    else:
        print(f"DQ check rules are not applied successfully.")

if __name__=='__main__':
    main()
