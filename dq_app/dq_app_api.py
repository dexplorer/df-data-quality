import os
import argparse
import logging

from dq_app.settings import ConfigParms as sc
from dq_app import dq_app_core as dqc
from utils import logger as ufl

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """
    Default route

    Args:
        none

    Returns:
        A default message.
    """

    return {"message": "Data Quality Validation App"}


@app.get("/apply-rules/")
async def apply_rules(dataset_id: str, cycle_date: str = ""):
    """
    Apply DQ rules for the dataset.
 
     Args:
        dataset_id: Id of the dataset.
        cycle_date: Cycle date

    Returns:
        Results from the DQ checks.
    """

    logging.info("Start applying DQ rules on the dataset %s", dataset_id)
    dq_check_results = dqc.apply_dq_rules(dataset_id=dataset_id, cycle_date=cycle_date)
    logging.info("Finished applying DQ rules on the dataset %s", dataset_id)

    return {"results": dq_check_results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Quality Application")
    parser.add_argument(
        "-e", "--env", help="Environment", const="dev", nargs="?", default="dev"
    )

    # Get the arguments
    args = vars(parser.parse_args())
    logging.info(args)
    env = args["env"]

    sc.load_config(env=env)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Starting the API service")

    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.cfg_file_path}/api_log.ini",
    )

    logging.info("Stopping the API service")
