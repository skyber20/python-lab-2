import os
import oslex
import sys
from constants import file_commands
from utils.my_logger import logger
from src.commands.command_history import run_history


def main() -> None:
    while sys.stdin:
        inp: str = input(f"{os.getcwd()}> ")
        logger.info(inp)
        run_history(inp=inp, show=False)

        if inp == 'exit':
            print("Bye")
            break

        clear_inp = inp.replace("'", '"').replace("\\", "/")
        tokens: list[str] = oslex.split(clear_inp)

        try:
            file_commands[tokens[0]](tokens[1:])
        except KeyError:
            logger.error(f"{tokens[0]}: Command not found")
            print(f"{tokens[0]}: Команда не найдена")


if __name__ == '__main__':
    main()
