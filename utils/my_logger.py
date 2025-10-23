import logging


logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('shell.log', mode='a')
handler.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='[ %(asctime)s ] %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.propagate = False


# logging.basicConfig(level=logging.INFO, filename='shell.log', format='[ %(asctime)s ] %(levelname)s: %(message)s',
#                     datefmt="%Y-%m-%d %H:%M:%S", filemode='a')
