import pytest
from dq_app import dq_app_core as dqc

test_data = [
    (
        "1",
        "2024-12-26",
        [
            {"expectation": "ExpectColumnValuesToBeUnique", "rule_id": "1", "result": 'Pass'},
            {"expectation": "ExpectColumnValuesToBeInSet", "rule_id": "2", "result": 'Pass'},
            {"expectation": "ExpectColumnValuesToBeBetween", "rule_id": "3", "result": 'Fail'},
        ],
    )
]


@pytest.mark.parametrize("dataset_id, cycle_date, dq_results_expected", test_data)
def test_apply_dq_rules(dataset_id: str, cycle_date: str, dq_results_expected: list):
    dq_results_actual = dqc.apply_dq_rules(dataset_id=dataset_id, cycle_date=cycle_date)

    assert dq_results_actual == dq_results_expected
