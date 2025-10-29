from pathlib import Path
from utils.my_logger import logger


def run_cat(inp: list[str] = []) -> None:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if options:
        logger.error(f"cd: '{options[0]}': invalid option")
        print(f"cd: '{options[0]}': invalid option")
        return

    for i in pathes:
        path: Path = Path(i)
        abs_path: Path = path.absolute()

        if abs_path.exists():
            print(f"{path}:")
            if abs_path.is_dir():
                logger.error(f"cat: {path} is a directory")
                print(f"Is a directory\n")
            else:
                try:
                    print(abs_path.read_text(encoding='utf-8'), end='\n\n')
                    logger.info(f"OK. command 'cat' is successful complete")
                except UnicodeDecodeError:
                    # print(abs_path.read_bytes(), end='\n\n')
                    logger.error(f"{path} is not a docx file")
                    print(f"{path} is not a docx file")
        else:
            logger.error(f"cat: cannot access {path}: No such file")
            print(f"cat: cannot access {path}: No such file\n")
