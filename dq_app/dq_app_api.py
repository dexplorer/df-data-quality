from dq_app import settings as sc
from dq_app import dq_app_core as dqc
from dq_app.utils import logger as ufl
import logging
import os

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """
    Default route
    """

    return {"message": "Data Quality Validation App"}


@app.get("/apply-rules/{dataset_id}")
async def apply_rules(dataset_id: str, env: str = "dev"):
    """
    Apply DQ rules for the dataset.
    See ./log/dq_app_cli.log for logs.
    """

    logging.info(f"Set configs")
    cfg = sc.load_config(env)
    sc.set_config(cfg)

    logging.info(f"Start applying DQ rules on the dataset {dataset_id}")
    dq_check_results = dqc.apply_dq_rules(dataset_id=dataset_id)

    logging.info(f"Finished applying DQ rules on the dataset {dataset_id}")

    return {"results": dq_check_results}


if __name__ == "__main__":
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_name=script_name)
    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.APP_ROOT_DIR}/log/dq_app_api_log.ini",
    )
