import logging
import os
from src.constants import SHELL_LOG


def setup_my_logger():
    my_logger_create = logging.getLogger('logger')
    my_logger_create.setLevel(logging.INFO)

    abs_shell_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', SHELL_LOG))
    handler = logging.FileHandler(abs_shell_log, mode='a')
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt='[ %(asctime)s ] %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

    handler.setFormatter(formatter)
    my_logger_create.addHandler(handler)

    my_logger_create.propagate = False

    return my_logger_create


logger = setup_my_logger()
