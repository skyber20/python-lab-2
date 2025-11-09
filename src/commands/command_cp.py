import shutil
import os
from utils.my_logger import logger
from utils.errors_handler import handle_error


def run_cp(inp: list[str]) -> dict[str, str | bool | os.PathLike] | bool:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if len(pathes) < 2:
        handle_error("invalid_amount_params", "cp", need_log=True)
        return False

    if len(set(options)) > 1:
        handle_error("invalid_amount_options", "cp", need_log=True)
        return False

    if options and options[0] != '-r':
        handle_error("invalid_option", "cp", options[0], need_log=True)
        return False

    last: str = os.path.abspath(pathes[-1])
    flag: bool = False

    for p in pathes[:-1]:
        source: str = os.path.abspath(p)

        if not os.path.exists(source):
            handle_error("path_not_found", "cp", p)
            continue

        if os.path.isdir(last):
            destination: str = os.path.join(last, os.path.basename(source))
        else:
            destination: str = last

        try:
            if os.path.isdir(source):
                if not options:
                    handle_error("need_option_not_found", "cp", "-r")
                    continue

                if not os.path.exists(os.path.dirname(destination)):
                    handle_error("path_not_found", "cp", last)
                    continue

                if os.path.exists(destination):
                    handle_error("already_exists", "cp", destination, need_log=True)
                    return False

                shutil.copytree(source, destination)
                flag = True
            elif os.path.isfile(source):
                if not os.path.exists(os.path.dirname(destination)):
                    handle_error("path_not_found", "cp", last)
                    continue

                if os.path.exists(destination):
                    handle_error("already_exists", "cp", destination, need_log=True)
                    return False

                shutil.copy(source, destination)
                flag = True
        except Exception:
            print(f'Не удалось скопировать {p} в {last}')

    if flag:
        logger.info("OK. command 'cp' is successful complete")
        return True

    return False
