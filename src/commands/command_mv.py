import os
from utils.my_logger import logger


def run_mv(inp: list[str]) -> dict[str, str | bool | os.PathLike] | bool:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if len(pathes) < 2:
        logger.error(f"mv: Not 2 paths were introduced")
        print(f"mv: Not 2 paths were introduced")
        return False

    if options:
        logger.error(f"mv: {options[0]}: Invalid option")
        print(f"mv: {options[0]}: Invalid option")
        return False

    last: str = os.path.abspath(pathes[-1])
    flag: bool = False

    for source in pathes[:-1]:
        abs_path: str = os.path.abspath(source)

        if os.path.exists(abs_path):
            if os.path.isdir(last):
                destination: str = os.path.join(last, os.path.basename(abs_path))
            else:
                destination: str = last

            try:
                os.rename(source, destination)
                flag = True
            except PermissionError:
                s: str = f"mv: {pathes[-1]}: Permission denied"
            except FileNotFoundError:
                s: str = f"mv: {pathes[-1]}: No such file or directory"
            except FileExistsError:
                s: str = f"mv: {os.path.basename(destination)}: such a file or folder already exists"
            except OSError:
                s: str = f"mv: cannot move {source} to {pathes[-1]}"

            if not flag:
                print(s)
        else:
            print(f"mv: {source}: No such file or directory")

    if flag:
        logger.info(f"OK. command 'mv' is successful complete")
        return True

    logger.error(s)
    return False


