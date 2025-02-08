import logging
import os

import click
from dq_app.settings import ConfigParms as sc
from dq_app import dq_app_core as dqc
from utils import logger as ufl


# Create command group
@click.group()
def cli():
    pass


@cli.command()
# @click.argument('dataset_id', required=1)
@click.option(
    "--dataset_id", type=str, default="dev", help="Source dataset id", required=True
)
@click.option("--env", type=str, default="dev", help="Environment")
@click.option("--cycle_date", type=str, default="", help="Cycle date")
def apply_rules(dataset_id: str, env: str, cycle_date: str):
    """
    Apply DQ rules for the dataset.
    """

    sc.load_config(env)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Start applying DQ rules on the dataset %s", dataset_id)
    dq_check_results = dqc.apply_dq_rules(dataset_id=dataset_id, cycle_date=cycle_date)

    logging.info("DQ check results for dataset %s", dataset_id)
    logging.info(dq_check_results)

    logging.info("Finished applying DQ rules on the dataset %s", dataset_id)

    return {"results": dq_check_results}


def main():
    cli()


if __name__ == "__main__":
    main()
