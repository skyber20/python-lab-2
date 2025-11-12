import shutil
import os
from src.commands.command_undo import save_action
from src import exceptions
from utils.my_logger import logger


def run_cp(inp: list[str]) -> None:
    options = []
    paths = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            paths.append(i)

    if len(paths) < 2:
        raise exceptions.InvalidAmountPaths('cp')

    if options:
        if len(set(options)) > 1:
            raise exceptions.InvalidAmountOptions('cp')
        if options[0] != '-r':
            raise exceptions.InvalidOption('cp', options[0])

    destination = os.path.abspath(paths[-1])
    k = 0
    dict_for_undo = {
        'command': 'cp',
        'sources': [],
        'destinations': [],
        'is_dirs': []
    }

    for path in paths[:-1]:
        source = os.path.abspath(path)

        if not os.path.exists(source):
            print(f'{path}: Нет такого пути')
            continue

        if os.path.isdir(source) and not options:
            print("Для копирования папки нужна опция -r")
            continue

        if os.path.isdir(destination):
            destination = os.path.join(destination, os.path.basename(source))

        if not os.path.exists(os.path.dirname(destination)):
            raise exceptions.PathNotExists('cp', os.path.dirname(destination))

        if os.path.exists(destination):
            print(f'{os.path.basename(destination)}: Путь уже существует')
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
        logger.info("cp: OK")
        return
    logger.error("cp: Не OK")
