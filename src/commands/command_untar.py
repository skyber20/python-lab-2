import tarfile
import os
from src import exceptions
from utils.my_logger import logger


def run_untar(inp: list[str]) -> None:
    if len(inp) != 1:
        raise exceptions.InvalidAmountArguments('untar')

    archive_path = os.path.abspath(inp[0])
    archive_path = archive_path if archive_path.endswith('.tar.gz') else archive_path + '.tar.gz'

    if not os.path.exists(archive_path):
        raise exceptions.PathNotExists('untar', os.path.basename(archive_path))

    try:
        with tarfile.open(archive_path, 'r:gz') as tarf:
            if not tarf.getmembers():
                raise exceptions.EmptyDir('untar', os.path.basename(archive_path))

            tarf.extractall(os.path.dirname(archive_path))
        logger.info('untar: OK')
    except Exception:
        print(f'Не удалось разархивировать {os.path.basename(archive_path)}')
        logger.error(f'Не удалось разархивировать {os.path.basename(archive_path)}')
