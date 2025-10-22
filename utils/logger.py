import logging

logging.basicConfig(level=logging.INFO, filename='shell.log', format='[ %(asctime)s ] %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S", filemode='a')
