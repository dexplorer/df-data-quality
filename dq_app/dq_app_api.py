from dq_app import settings as sc
from dq_app import dq_app_core as dqc
import logging

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """
    Default route
    """

    return {"message": "Data Quality Validation App"}


@app.get("/apply-rules/{dataset_id}/{cycle_date}")
async def apply_rules(dataset_id: str, env: str = "dev", cycle_date: str = ""):
    """
    Apply DQ rules for the dataset.
    """

    sc.load_config(env)

    logging.info("Configs are set")

    logging.info("Start applying DQ rules on the dataset %s", dataset_id)
    dq_check_results = dqc.apply_dq_rules(dataset_id=dataset_id, cycle_date=cycle_date)

    logging.info("Finished applying DQ rules on the dataset %s", dataset_id)

    return {"results": dq_check_results}


if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.APP_ROOT_DIR}/cfg/dq_app_api_log.ini",
    )
