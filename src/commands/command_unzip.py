import zipfile
import os
from src import exceptions
from utils.my_logger import logger


def run_unzip(inp: list[str]) -> None:
    if len(inp) != 1:
        raise exceptions.InvalidAmountArguments('unzip')

    archive_path = os.path.abspath(inp[0])
    archive_path = archive_path if archive_path.endswith('.zip') else archive_path + '.zip'

    if not os.path.exists(archive_path):
        raise exceptions.PathNotExists('unzip', os.path.basename(archive_path))

    try:
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            if not zipf.namelist():
                raise exceptions.EmptyDir('unzip', os.path.basename(archive_path))

            zipf.extractall(os.path.dirname(archive_path))
        logger.info('unzip: OK')
    except Exception as e:
        print(f'Не удалось разархивировать {os.path.basename(archive_path)}')
        logger.error(f'Не удалось разархивировать {os.path.basename(archive_path)}')
