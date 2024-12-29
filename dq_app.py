import settings as sc

import os
import argparse
import logging

import dq_app_core as dqc


def main():
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    log_file = f"./log/{script_name}.log"
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(filename)s (%(lineno)d) : %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
        level=logging.INFO,
        filename=log_file,
        filemode="w",
    )
    logging.captureWarnings(True)
    # logging.FileHandler(filename, mode='a', encoding=None, delay=False)

    parser = argparse.ArgumentParser(description="Data Quality Validation Application")
    parser.add_argument(
        "-e", "--env", help="Environment", const="dev", nargs="?", default="dev"
    )
    parser.add_argument(
        "-s",
        "--src",
        help="Source data",
        const="1",
        nargs="?",
        default="1",
        required=True,
    )

    # Sample invocation
    # python dq_app.py --env='dev'

    logging.info(f"Starting {script_name}")

    # Get the arguments
    args = vars(parser.parse_args())
    logging.info(args)
    env = args["env"]
    src_dataset_id = args["src"]

    cfg = sc.load_config(env)  # pass ENV from command line argument later
    sc.set_config(cfg)
    # print(sc.source_file_path)
    logging.info(cfg)

    dq_check_results = dqc.apply_dq_rules(dataset_id=src_dataset_id)

    print(f"DQ check results for dataset {src_dataset_id}")
    print(dq_check_results)

    logging.info(f"Finishing {script_name}")


if __name__ == "__main__":
    main()
