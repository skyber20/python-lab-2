import os.path
from utils.my_logger import logger
from utils.errors_handler import handle_error


def run_cd(inp: list[str] = []) -> None:
    if len(inp) > 1:
        handle_error("invalid_amount_params", "cd", need_log=True)
        return

    elif not inp:
        logger.info("OK. command 'cd' is successful complete")
        os.chdir(os.path.expanduser('~'))
        return

    elif inp[0].startswith('-'):
        handle_error("invalid_option", "cd", inp[0], need_log=True)
        return

    if inp[0].startswith('~'):
        inp[0] = inp[0].replace('~', os.path.expanduser('~').replace("\\", "/"))
    abspath: str = inp[0] if os.path.isabs(inp[0]) else os.path.abspath(inp[0])

    if os.path.exists(abspath):
        if os.path.isdir(abspath):
            logger.info("OK. command 'cd' is successful complete")
            os.chdir(abspath)
        else:
            logger.error(f"cd: {inp[0]}: Not a directory")
            print(f"cd: {inp[0]}: Не папка")
    else:
        handle_error("path_not_found", "cd", inp[0], need_log=True)
