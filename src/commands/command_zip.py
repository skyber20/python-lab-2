import zipfile
import os


def is_folder_empty(folder: str) -> bool:
    for file_dir in os.scandir(folder):
        if os.path.isfile(file_dir):
            return False
        if not is_folder_empty(file_dir.path):
            return False
    return True


def run_zip(inp: list[str]) -> None:
    if len(inp) != 2:
        print("нужны 2 аргумента")
        return

    folder_path: str = os.path.abspath(inp[0])
    archive_path: str = os.path.abspath(inp[1])

    if not os.path.isdir(folder_path):
        print(f"{inp[0]}: Не папка")
        return

    if is_folder_empty(folder_path):
        print(f"{inp[0]}: Папка пустая. Не получится архивировать")
        return

    archive_path = archive_path if archive_path.endswith(".zip") else archive_path + ".zip"

    if not os.path.exists(os.path.dirname(archive_path)):
        print(f"{inp[1]}: Невозможно архивировать папку в несуществующий путь")
        return

    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path: str = os.path.join(root, file)
                    rel: str = os.path.relpath(file_path, os.path.dirname(folder_path))
                    zipf.write(file_path, arcname=rel)
    except Exception as e:
        print('1', e)
