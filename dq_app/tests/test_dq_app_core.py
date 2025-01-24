import pytest
from dq_app import dq_app_core as dqc

test_data = [
    (
        "1",
        [
            {"rule_id": "1", "result": True},
            {"rule_id": "2", "result": True},
            {"rule_id": "3", "result": False},
        ],
    )
]


@pytest.mark.parametrize("dataset_id, dq_results_expected", test_data)
def test_apply_dq_rules(dataset_id: str, dq_results_expected: list):
    dq_results_actual = dqc.apply_dq_rules(dataset_id)

    assert dq_results_actual == dq_results_expected
