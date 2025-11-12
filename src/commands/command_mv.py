import os
from src.commands.command_undo import save_action
from src import exceptions
from utils.my_logger import logger


def run_mv(inp: list[str]) -> None:
    options = []
    paths = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            paths.append(i)

    if len(paths) < 2:
        raise exceptions.InvalidAmountPaths('mv')

    if options:
        raise exceptions.InvalidAmountOptions('mw')

    dest = os.path.abspath(paths[-1])
    k = 0
    dict_for_undo = {
        'command': 'mv',
        'sources': [],
        'destinations': []
    }

    for p in paths[:-1]:
        source = os.path.abspath(p)

        if not os.path.exists(source):
            print("Нет такого пути")
            continue

        if os.path.isdir(dest):
            destination = os.path.join(dest, os.path.basename(source))
        else:
            destination = dest

        if os.path.exists(destination):
            print(f"{os.path.basename(destination)} уже существует")
            continue

        try:
            os.rename(source, destination)
            dict_for_undo['sources'].append(source)
            dict_for_undo['destinations'].append(destination)
            k += 1
        except Exception:
            print('Не удалось переместить папку/файл')

    if k:
        save_action(dict_for_undo)
        logger.info(f"mv: OK")
        return
    logger.error("mv: Не OK")
