import tarfile
import os
from src import exceptions
from utils.my_logger import logger


def is_folder_empty(folder: str) -> bool:
    for file_dir in os.scandir(folder):
        if os.path.isfile(file_dir):
            return False
        if not is_folder_empty(file_dir.path):
            return False
    return True


def run_tar(inp: list[str]) -> None:
    if len(inp) != 2:
        raise exceptions.InvalidAmountArguments('tar')

    folder_path = os.path.abspath(inp[0])
    archive_path = os.path.abspath(inp[1])

    if not os.path.isdir(folder_path):
        raise exceptions.IsNotDir('tar', os.path.basename(folder_path))

    if is_folder_empty(folder_path):
        raise exceptions.EmptyDir('tar', os.path.basename(folder_path))

    archive_path = archive_path if archive_path.endswith(".tar.gz") else archive_path + ".tar.gz"

    if not os.path.exists(os.path.dirname(archive_path)):
        raise exceptions.PathNotExists('tar', os.path.dirname(archive_path))

    try:
        with tarfile.open(archive_path, 'w:gz') as tarf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel = os.path.relpath(file_path, os.path.dirname(folder_path))
                    tarf.add(file_path, arcname=rel)
        logger.info('tar: OK')
    except Exception:
        print(f'Не удалось архивировать {os.path.basename(folder_path)}')
        logger.error(f'Не удалось архивировать {os.path.basename(folder_path)}')
