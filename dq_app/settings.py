import confuse

import logging

config = confuse.Configuration("dq_app", __name__)

global APP_ROOT_DIR
APP_ROOT_DIR = f"/workspaces/df-data-quality/dq_app"

# Define config variables at module scope
log_file_path = "" 
source_file_path = ""
api_data_path = ""
api_datasets_file = ""
api_dq_expectations_file = ""
api_dq_rules_file = ""


def load_config(env):
    try:
        if env == "prod":
            config.set_file(f"{APP_ROOT_DIR}/cfg/config.yaml")
        elif env == "qa":
            config.set_file(f"{APP_ROOT_DIR}/cfg/config_qa.yaml")
        elif env == "dev":
            config.set_file(f"{APP_ROOT_DIR}/cfg/config_dev.yaml")
        else:
            raise ValueError(
                "Environment is invalid. Accepted values are prod / qa / dev ."
            )
    except ValueError as error:
        logging.error(error)
        raise

    cfg = config["CONFIG"].get()

    logging.info(cfg)
    return cfg


def set_config(cfg):
    global log_file_path
    log_file_path = f"{resolve_app_path(cfg['log_file_path'])}"

    global source_file_path
    source_file_path = f"{resolve_app_path(cfg['source_file_path'])}"

    global api_data_path
    api_data_path = f"{resolve_app_path(cfg['api_data_path'])}"
    logging.info(api_data_path)

    global api_datasets_file
    api_datasets_file = cfg["api_datasets_file"]

    global api_dq_expectations_file
    api_dq_expectations_file = cfg["api_dq_expectations_file"]

    global api_dq_rules_file
    api_dq_rules_file = cfg["api_dq_rules_file"]


def resolve_app_path(rel_path):
    return rel_path.replace("APP_ROOT_DIR", APP_ROOT_DIR)
