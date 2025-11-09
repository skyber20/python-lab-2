from pathlib import Path
from utils.my_logger import logger
from utils.errors_handler import handle_error


def run_cat(inp: list[str] = []) -> None:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if options:
        handle_error("invalid_option", "cat", options[0], need_log=True)
        return

    for i in pathes:
        path: Path = Path(i)
        abs_path: Path = path.absolute()

        if abs_path.exists():
            if abs_path.is_dir():
                logger.error(f"cat: {path} is a directory")
                print(f"cat: {path}: Это папка\n")
            else:
                try:
                    print(abs_path.read_text(encoding='utf-8'), end='\n\n')
                    logger.info(f"OK. command 'cat' is successful complete")
                except UnicodeDecodeError:
                    logger.error(f"cat: {path}: is not a docx file")
                    print(f"cat: {path}: это не текстовый документ")
        else:
            handle_error("path_not_found", "cat", path, need_log=True)
