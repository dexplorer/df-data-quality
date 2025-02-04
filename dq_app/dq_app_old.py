from dq_app import settings as sc

import os
import argparse
import logging

from dq_app import dq_app_core as dqc
from utils import logger as ufl


def main():
    parser = argparse.ArgumentParser(description="Data Quality Validation Application")
    parser.add_argument(
        "-e", "--env", help="Environment", const="dev", nargs="?", default="dev"
    )
    parser.add_argument(
        "-d",
        "--dataset_id",
        help="Source data",
        const="1",
        nargs="?",
        default="1",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--cycle_date",
        help="Cycle date",
        const="1",
        nargs="?",
        default="",
        required=False,
    )

    # Sample invocation
    # python dq_app.py --env='dev'

    script_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.info("Starting %s", script_name)

    # Get the arguments
    args = vars(parser.parse_args())
    logging.info(args)
    env = args["env"]
    src_dataset_id = args["dataset_id"]
    cycle_date = args["cycle_date"]

    sc.load_config(env)
    # print(sc.source_file_path)

    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    dq_check_results = dqc.apply_dq_rules(
        dataset_id=src_dataset_id, cycle_date=cycle_date
    )

    print("DQ check results for dataset %s", src_dataset_id)
    print(dq_check_results)

    logging.info("Finishing %s", script_name)


if __name__ == "__main__":
    main()
