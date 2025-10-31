import tarfile
import zipfile
import os


def run_untar(inp: list[str]) -> None:
    if len(inp) != 1:
        print("нужен 1 аргумент")
        return

    archive_path: str = os.path.abspath(inp[0])
    archive_path = archive_path if archive_path.endswith('.tar.gz') else archive_path + '.tar.gz'

    if not os.path.exists(archive_path):
        print("Архива не существует")
        return

    try:
        with tarfile.open(archive_path, 'r:gz') as tarf:
            if not tarf.getmembers():
                print("Архив пустой. Не получится разархивировать")
                return

            tarf.extractall(os.path.dirname(archive_path))
    except Exception as e:
        print(e)


