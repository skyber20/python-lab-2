import os
from constants import file_commands
from utils.my_logger import logger


def main() -> None:
    while True:
        inp: list[str] = input(f"{os.getcwd()}> ").split()

        if inp[0] == 'exit':
            break

        logger.info(' '.join(inp))

        try:
            file_commands[inp[0]](inp[1:])
        except KeyError:
            logger.error(f"command '{inp[0]}' not found")
            print(f"command '{inp[0]}' not found")


if __name__ == '__main__':
    main()
