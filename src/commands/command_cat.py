from pathlib import Path
from utils.my_logger import logger


def run_cat(inp: list[str] = []) -> None:
    for i in inp:
        if i.startswith('-'):
            logger.error(f"cd: '{i}': invalid option")
            print(f"cd: '{i}': invalid option")
            return

        path: Path = Path(i)
        abs_path: Path = path.absolute()

        if abs_path.exists():
            print(f"{path}:")
            if abs_path.is_dir():
                logger.error(f"cat: {path} is a directory")
                print(f"Is a directory\n")
            else:
                logger.info(f"OK. command 'cat' is successful complete")
                try:
                    print(abs_path.read_text(encoding='utf-8'), end='\n\n')
                except UnicodeDecodeError:
                    print(abs_path.read_bytes(), end='\n\n')
        else:
            logger.error(f"cat: cannot access {path}: No such file")
            print(f"cat: cannot access {path}: No such file\n")
