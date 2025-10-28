import os
import oslex
from constants import file_commands
from utils.my_logger import logger


def main() -> None:
    while True:
        inp: str = input(f"{os.getcwd()}> ")
        logger.info(inp)
        clear_inp = inp.replace("'", '"').replace("\\", "/")
        tokens: list[str] = oslex.split(clear_inp)

        try:
            file_commands[tokens[0]](tokens[1:])
        except KeyError:
            logger.error(f"command '{tokens[0]}' not found")
            print(f"command '{tokens[0]}' not found")


if __name__ == '__main__':
    main()
