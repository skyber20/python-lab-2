import zipfile
import os


def run_unzip(inp: list[str]) -> None:
    if len(inp) != 1:
        print("нужен 1 аргумент")
        return

    archive_path: str = os.path.abspath(inp[0])
    archive_path = archive_path if archive_path.endswith('.zip') else archive_path + '.zip'

    if not os.path.exists(archive_path):
        print("Архива не существует")
        return

    try:
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            if not zipf.namelist():
                print("Архив пустой. Не получится разархивировать")
                return

            zipf.extractall(os.path.dirname(archive_path))
    except Exception as e:
        print(e)


