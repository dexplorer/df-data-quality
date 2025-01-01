import logging
import os

# import sys
# sys.path.insert(1, "./utils")
# print(sys.path)
import click
from dq_app import settings as sc
from dq_app import dq_app_core as dqc
from dq_app.utils import logger as ufl


@click.command()
# @click.argument('dataset_id', required=1)
@click.option(
    "--dataset_id", type=str, default="dev", help="Source dataset id", required=True
)
@click.option("--env", type=str, default="dev", help="Environment")
def apply_rules(dataset_id: str, env: str):
    """
    Apply DQ rules for the dataset.
    See ./log/dq_app_cli.log for logs.
    """

    logging.info(f"Set configs")
    cfg = sc.load_config(env)
    sc.set_config(cfg)

    logging.info(f"Start applying DQ rules on the dataset {dataset_id}")
    dq_check_results = dqc.apply_dq_rules(dataset_id=dataset_id)

    click.echo(f"DQ check results for dataset {dataset_id}")
    click.echo(dq_check_results)

    logging.info(f"Finished applying DQ rules on the dataset {dataset_id}")


# Create command group
@click.group()
def cli():
    pass


# Add sub command to group
cli.add_command(apply_rules)


def main():
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_name=script_name)
    cli()


if __name__ == "__main__":
    main()
