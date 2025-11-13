import os.path
from src import exceptions
from utils.my_logger import logger


def run_cd(inp: list[str]) -> None:
    if len(inp) > 1:
        raise exceptions.InvalidAmountArguments('cd')

    elif not inp:
        logger.info("cd: OK")
        os.chdir(os.path.expanduser('~'))
        return

    elif inp[0].startswith('-'):
        raise exceptions.InvalidOption('cd', inp[0])

    if inp[0].startswith('~'):
        inp[0] = inp[0].replace('~', os.path.expanduser('~').replace("\\", "/"))
    abspath = inp[0] if os.path.isabs(inp[0]) else os.path.abspath(inp[0])

    if os.path.exists(abspath):
        if os.path.isdir(abspath):
            logger.info("cd: OK")
            os.chdir(abspath)
        else:
            raise exceptions.IsNotDir('cd', os.path.basename(inp[0]))
    else:
        raise exceptions.PathNotExists('cd', os.path.basename(inp[0]))
