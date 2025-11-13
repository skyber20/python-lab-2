import os
from datetime import datetime
from src.constants import TRASH_DIR
from src.commands.command_undo import save_action
from src import exceptions
from utils.my_logger import logger


def create_trash() -> str:
    cur_dir = os.path.dirname(__file__)
    abs_trash = os.path.abspath(os.path.join(cur_dir, '..', '..', TRASH_DIR))

    if not os.path.exists(abs_trash):
        os.makedirs(abs_trash)

    return abs_trash


def is_protected_path(path: str) -> bool:
    root_path = os.path.abspath('/')
    current_dir = os.path.abspath('.')

    if path in [root_path, current_dir]:
        print('Невозможно удалить текущий и корневой каталоги')
        return True

    if current_dir.startswith(path):
        print('Невозможно удалить родительскую папку')
        return True

    return False


def del_file_dir(abs_path: str, trash_dir: str) -> str:
    name = os.path.basename(abs_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    name_to_trash = f"{timestamp}_{name}"
    path_to_trash = os.path.join(trash_dir, name_to_trash)

    os.rename(abs_path, path_to_trash)
    return path_to_trash


def run_rm(inp: list[str]) -> None:
    options = []
    paths = []
    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            paths.append(i)

    if not paths:
        raise exceptions.InvalidAmountPaths('rm')

    if options:
        if len(set(options)) > 1:
            raise exceptions.InvalidAmountOptions('rm')
        if options[0] != '-r':
            raise exceptions.InvalidOption('rm', options[0])

    trash_dir = create_trash()
    k = 0
    answer_y = True
    dict_for_undo = {
        'command': 'rm',
        'sources': [],
        'destinations': [],
    }

    for p in paths:
        source = os.path.abspath(p)
        if is_protected_path(source):
            continue

        if not os.path.exists(source):
            print("Нет такого пути")
            continue

        if os.path.isdir(source) and not options:
            print("Для удаления папки нужна опция -r")
            continue

        sure = input(f"{p}: y/n ").lower()
        if sure != 'y':
            answer_y = False
            continue

        try:
            path_to_trash = del_file_dir(source, trash_dir)
            dict_for_undo['sources'].append(source)
            dict_for_undo['destinations'].append(path_to_trash)
            k += 1
        except Exception:
            print("Не удалось удалить папку/файл")

    if k:
        logger.info('rm: OK')
        save_action(dict_for_undo)
        return
    elif not answer_y:
        logger.info('rm: OK')
        return
    logger.error("rm: Не OK")
