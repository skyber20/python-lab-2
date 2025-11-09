import os
from datetime import datetime
from utils.my_logger import logger
from src.constants import TRASH_DIR
from src.commands.command_undo import save_action


def create_trash() -> str:
    cur_dir: str = os.path.dirname(__file__)
    abs_trash: str = os.path.abspath(os.path.join(cur_dir, '..', '..', TRASH_DIR))

    if not os.path.exists(abs_trash):
        os.makedirs(abs_trash)

    return abs_trash


def del_file_dir(abs_path: str, trash_dir: str) -> str:
    name: str = os.path.basename(abs_path)
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    name_to_trash: str = f"{timestamp}_{name}"
    path_to_trash: str = os.path.join(trash_dir, name_to_trash)

    os.rename(abs_path, path_to_trash)
    return path_to_trash


def run_rm(inp: list[str]) -> None:
    options: list[str] = []
    pathes: list[str] = []
    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if not pathes:
        logger.error("at least 1 path must be entered")
        print("rm: At least 1 path must be entered")
        return

    if len(set(options)) > 1:
        logger.error(f"rm: Only one option can be introduced")
        print(f"rm: Only one option can be introduced")
        return

    if options and options[0] != '-r':
        logger.error(f"rm: {options[0]}: invalid option")
        print(f"rm: {options[0]}: invalid option")
        return

    trash_dir = create_trash()
    k = 0
    answer_y = True
    dict_for_undo = {
        'command': 'rm',
        'sources': [],
        'destinations': [],
    }

    for p in pathes:
        source = os.path.abspath(p)
        if p in ['/', '.', '..'] or source == os.path.abspath('.'):
            s: str = "rm: cannot be deleted '.', '..', '/'"
            print(s)
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
        save_action(dict_for_undo)
        return
    elif not answer_y:
        return
    logger.error("rm: Error")
