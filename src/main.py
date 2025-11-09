import os
import oslex
import sys
from command_registry import file_commands
from utils.my_logger import logger
from utils.errors_handler import handle_error
from src.commands.command_history import run_history


def main() -> None:
    while sys.stdin:
        inp = input(f"{os.getcwd()}> ")
        logger.info(inp)
        run_history(inp=inp, show=False)

        if inp == 'exit':
            print("Bye")
            break

        if inp == 'help':
            dict_descr_cmds = {}
            continue

        clear_inp = inp.replace("'", '"').replace("\\", "/")
        tokens = oslex.split(clear_inp)

        try:
            file_commands[tokens[0]](tokens[1:])
        except KeyError:
            handle_error("command_not_found", tokens[0], need_log=True)


if __name__ == '__main__':
    main()
