import os
import logging


def config_logger(log_file_name):
    log_file = f"./dq_app/log/{log_file_name}.log"
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(filename)s (%(lineno)d) : %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
        level=logging.INFO,
        filename=log_file,
        filemode="w",
    )
    logging.captureWarnings(True)
    # logging.FileHandler(filename, mode='a', encoding=None, delay=False)
