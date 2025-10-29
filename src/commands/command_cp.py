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

    if len(pathes) != 2:
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

    source: str = os.path.abspath(pathes[0])
    destination: str = os.path.abspath(pathes[1])

    if os.path.exists(source):
        if os.path.isfile(source):
            try:
                shutil.copy(source, destination)
                logger.info(f"OK. command 'cp' is successful complete")
                return {
                    'status': True
                }
            except PermissionError:
                logger.error(f"cp: {pathes[1]}: Permission denied")
                print(f"cp: {pathes[1]}: Permission denied")
            except FileNotFoundError:
                logger.error(f"cp: cannot create {pathes[1]}")
                print(f"cp: cannot create {pathes[1]}")
            finally:
                return {
                    'status': False
                }

        if options:
            if os.path.exists(os.path.split(destination)[0]):
                try:
                    shutil.copytree(source, destination, dirs_exist_ok=True, copy_function=shutil.copy)
                    logger.info(f"OK. command 'cp -r' is successful complete")
                    return {
                        'status': True
                    }
                except PermissionError:
                    logger.error(f"cp: {pathes[1]}: Permission denied")
                    print(f"cp: {pathes[1]}: Permission denied")
                except FileExistsError:
                    logger.error(f"cp: cannot overwrite non-directory {pathes[1]} with directory {pathes[0]}")
                    print(f"cp: cannot overwrite non-directory {pathes[1]} with directory {pathes[0]}")
                finally:
                    return {
                        'status': False
                    }

            logger.error(f"cp: cannot create {pathes[1]}")
            print(f"cp: cannot create {pathes[1]}")
            return {
                'status': False
            }

        logger.error(f"Need option -r for copy catalog")
        print(f"Need option -r for copy catalog")
        return {
            'status': False
        }

    logger.error(f"cp: {pathes[0]}: No such file or directory")
    print(f"cp: {pathes[0]}: No such file or directory")
    return {
        'status': False
    }

