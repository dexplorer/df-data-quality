import pytest
import dq_expectation as dqe
import dq_app_core as dqc

test_data = [
    (
        "1",
        dqe.DQExpectation(
            exp_id="1",
            exp_name="ExpectColumnValuesToBeUnique",
            ge_method="ExpectColumnValuesToBeUnique",
        ),
    )
]


@pytest.mark.parametrize("exp_id, dq_expectation_expected", test_data)
def test_get_expectation_by_id(exp_id: str, dq_expectation_expected: dqe.DQExpectation):
    dq_expectation_expected = dqc.get_expectation_by_id(exp_id)

    assert dq_expectation_actual == dq_expectation_expected


# test_data2 = [
#     (
#         "1",
#         [
#             {"rule_id": "1", "result": True},
#             {"rule_id": "2", "result": True},
#             {"rule_id": "3", "result": False},
#         ],
#     )
# ]


# @pytest.mark.parametrize("dataset_id, dq_results_expected", test_data)
# def test_apply_dq_rules(dataset_id: str, dq_results_expected: list):
#     dq_results_actual = dqc.apply_dq_rules(dataset_id)

#     assert dq_results_actual == dq_results_expected
