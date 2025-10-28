import os.path
from utils.my_logger import logger


def run_cd(inp: list[str] = []) -> None:
    if len(inp) > 1:
        logger.error("cd: too many arguments")
        print("cd: too many arguments")
        return

    elif not inp:
        logger.info("OK. command 'cd' is successful complete")
        os.chdir(os.path.expanduser('~'))
        return

    elif inp[0].startswith('-'):
        logger.error(f"cd: '{inp[0]}': invalid option")
        print(f"cd: '{inp[0]}': invalid option")
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
            print(f"cd: {inp[0]}: Not a directory")
    else:
        logger.error(f"cd: {inp[0]}: No such file or directory")
        print(f"cd: {inp[0]}: No such file or directory")
