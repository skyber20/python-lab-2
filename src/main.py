import os
import oslex
import sys
import logging
from command_registry import file_commands
from src.commands.command_history import run_history
from src.constants import enum_exceptions


def main() -> None:
    while sys.stdin:
        inp = input(f"{os.getcwd()}> ")
        logger = logging.getLogger('logger')
        logger.info(inp)
        run_history(inp=inp, show=False)

        if inp == 'exit':
            print("Bye")
            break

        clear_inp = inp.replace("'", '"').replace("\\", "/")
        tokens = oslex.split(clear_inp)

        try:
            file_commands[tokens[0]](tokens[1:])
        except KeyError:
            print(f'{tokens[0]}: Такая команда не поддерживается')
            logger.error(f'{tokens[0]}: Такая команда не поддерживается')
        except enum_exceptions as e:
            print(e)
            logger.error(str(e))


if __name__ == '__main__':
    main()
