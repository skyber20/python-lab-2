import shutil
import os
from utils.my_logger import logger
from utils.errors_handler import handle_error
from src.commands.command_undo import save_action


def run_cp(inp: list[str]) -> None:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if len(pathes) < 2:
        handle_error("invalid_amount_params", "cp", need_log=True)
        return

    if len(set(options)) > 1:
        handle_error("invalid_amount_options", "cp", need_log=True)
        return

    if options and options[0] != '-r':
        handle_error("invalid_option", "cp", options[0], need_log=True)
        return

    destination = os.path.abspath(pathes[-1])
    k = 0
    dict_for_undo = {
        'command': 'cp',
        'sources': [],
        'destinations': [],
        'is_dirs': []
    }

    for p in pathes[:-1]:
        source = os.path.abspath(p)

        if not os.path.exists(source):
            handle_error("path_not_found", "cp", p)
            continue

        if os.path.isdir(source) and not options:
            print("Для копирования папки нужна опция -r")
            continue

        if os.path.isdir(destination):
            destination = os.path.join(destination, os.path.basename(source))

        if not os.path.exists(os.path.dirname(destination)):
            print(f"{os.path.dirname(destination)}: нельзя копировать папку/файл по несуществующему пути")
            continue

        if os.path.exists(destination):
            print(f"{os.path.basename(destination)} уже существует")
            continue

        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
                dict_for_undo['is_dirs'].append(True)
            elif os.path.isfile(source):
                shutil.copy(source, destination)
                dict_for_undo['is_dirs'].append(False)
            dict_for_undo['sources'].append(source)
            dict_for_undo['destinations'].append(destination)
            k += 1
        except Exception:
            print(f'Не удалось скопировать папку/файл')

    if k:
        save_action(dict_for_undo)
        logger.info("OK. command 'cp' is successful complete")
        return
    logger.error("rm: Error")
