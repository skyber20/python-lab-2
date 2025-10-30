import shutil
import os
from utils.my_logger import logger


def run_cp(inp: list[str]) -> dict[str, str | bool | os.PathLike]:
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
        return {
            'status': 'False'
        }

    if len(set(options)) > 1:
        logger.error(f"Only one option can be introduced")
        print(f"Only one option can be introduced")
        return {
            'status': 'False'
        }

    if options and options[0] != '-r':
        logger.error(f"cat: {options[0]}: invalid option")
        print(f"cp: {options[0]}: invalid option")
        return {
            'status': False
        }

    destination: str = os.path.abspath(pathes[-1])
    k: int = 0
    exist_pathes: set[str] = set()
    for elem in pathes[:-1]:
        abs_path: str = os.path.abspath(elem)
        if os.path.exists(abs_path):
            exist_pathes.add(abs_path)
            k += 1
        else:
            print(f"cp: {elem}: No such file or directory")
            
    if len(pathes) == 2 and not exist_pathes:
        logger.error(f"cp: {pathes[0]}: No such file or directory")
        print(f"cp: {pathes[0]}: No such file or directory")
        return {
            'status': False
        }

    if os.path.exists(destination):
        is_dir: bool = os.path.isdir(destination)
    else:
        is_dir: bool = k > 1 or destination[-1] in ['/', '\\']

    for source in exist_pathes:
        if os.path.isfile(source):
            try:
                shutil.copy(source, destination)
                flag = True
                logger.info(f"OK. command 'cp' is successful complete")
            except PermissionError:
                logger.error(f"cp: {pathes[-1]}: Permission denied")
                print(f"cp: {pathes[-1]}: Permission denied")
            except FileNotFoundError:
                logger.error(f"cp: cannot create {pathes[-1]}")
                print(f"cp: cannot create {pathes[-1]}")
        elif options:
            if os.path.exists(os.path.split(destination)[0]):
                try:
                    shutil.copytree(source, destination, dirs_exist_ok=True, copy_function=shutil.copy)
                    flag = True
                    logger.info(f"OK. command 'cp -r' is successful complete")
                except PermissionError:
                    logger.error(f"cp: {pathes[-1]}: Permission denied")
                    print(f"cp: {pathes[-1]}: Permission denied")
                except FileExistsError:
                    logger.error(f"cp: cannot overwrite non-directory {pathes[-1]} with directory {elem}")
                    print(f"cp: cannot overwrite non-directory {pathes[-1]} with directory {elem}")
            else:
                logger.error(f"cp: cannot create {pathes[-1]}")
                print(f"cp: cannot create {pathes[-1]}")
        else:
            logger.error(f"Need option -r for copy catalog")
            print(f"Need option -r for copy catalog")
            return {
                'status': False
            }


    if flag:
        return {
            'status': flag
        }

    return {
        'status': flag
    }