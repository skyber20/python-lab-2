import shutil
import os
from utils.my_logger import logger


def run_cp(inp: list[str]) -> dict[str, str | bool | os.PathLike] | bool:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if len(pathes) < 2:
        logger.error(f"Not 2 paths were introduced")
        print(f"Not 2 paths were introduced")
        return False

    if len(set(options)) > 1:
        logger.error(f"Only one option can be introduced")
        print(f"Only one option can be introduced")
        return False

    if options and options[0] != '-r':
        logger.error(f"cat: {options[0]}: invalid option")
        print(f"cp: {options[0]}: invalid option")
        return False

    last: str = os.path.abspath(pathes[-1])
    flag: bool = False

    for p in pathes[:-1]:
        source: str = os.path.abspath(p)

        if not os.path.exists(source):
            continue

        if os.path.isdir(last):
            destination: str = os.path.join(last, os.path.basename(source))
        else:
            destination: str = last

        try:
            if os.path.isdir(source):
                if not options:
                    print('...')
                    continue

                if not os.path.exists(os.path.dirname(destination)):
                    print('...')
                    continue

                if os.path.exists(destination):
                    print('...')
                    continue

                shutil.copytree(source, destination)
                flag = True
            elif os.path.isfile(source):
                if not os.path.exists(os.path.dirname(destination)):
                    print('...')
                    continue

                if os.path.exists(destination):
                    print('...')
                    continue

                shutil.copy(source, destination)
                flag = True
        except Exception:
            print('e')

    if flag:
        return True

    return False
