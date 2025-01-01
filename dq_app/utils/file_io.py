import logging


def uf_open_file(file_path: str, open_mode: str):
    """
    Open a file with exception handling.

    :param file_path: File path
    :type file_path: str
    :param open_mode: File open mode
    :type open_mode: str
    :return: File object
    :rtype: TextIOWrapper
    """

    try:
        f = open(file_path, open_mode)
    except FileNotFoundError as error:
        logging.error(error)
        raise  # re-raise error with stack trace
        # raise FileNotFoundError   # Don't do this, you'll lose the stack trace!
    else:
        return f
