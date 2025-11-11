import logging
import os
from src.constants import SHELL_LOG

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

abs_shell_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', SHELL_LOG))
handler = logging.FileHandler(abs_shell_log, mode='a')
handler.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='[ %(asctime)s ] %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.propagate = False
