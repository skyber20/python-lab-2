import json
import os
import shutil
from src.constants import UNDO_FILE


def create_undo_file() -> str:
    cur_dir: str = os.path.dirname(__file__)
    abs_undo_file: str = os.path.abspath(os.path.join(cur_dir, '..', '..', UNDO_FILE))

    if not os.path.exists(abs_undo_file):
        with open(abs_undo_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

    return abs_undo_file


def save_action(inp: dict[str, str | list[str | bool]]) -> None:
    undo_file = create_undo_file()
    with open(undo_file, 'r', encoding='utf-8') as f:
       actions = json.load(f)

    actions.append(inp)

    with open(undo_file, 'w', encoding='utf-8') as f:
        json.dump(inp, f, ensure_ascii=False, indent=2)


def check_exist_paths(sources: list[str], destinations: list[str]) -> bool:
    flag = True
    for source, dest in zip(destinations, sources):
        if not os.path.exists(source):
            flag = False
            print(f"{os.path.basename(source)}: такого пути нет")
        if not os.path.exists(os.path.dirname(dest)):
            flag = False
            print(f"{os.path.dirname(dest)}: невозможно переместить папку/файл по несуществующему")
        if not flag:
            return False
    return True


def execute_undo_action(inp: dict[str, str | list[str | bool]]) -> bool:
    command = inp['command']
    sources = inp['sources']
    destinations = inp['destinations']
    success = check_exist_paths(sources, destinations)

    if not success:
        return False

    if command == 'cp':
        is_dirs = inp['is_dirs']
        for dest, is_dir in zip(destinations, is_dirs):
            if is_dir:
                shutil.rmtree(dest)
            else:
                os.remove(dest)
    elif command == 'mv' or command == 'rm':
        for source, dest in zip(destinations, sources):
            os.rename(source, dest)

    return success


def run_undo(inp: list[str]) -> None:
    if inp:
        print("какие то аргументы ненужные")
        return

    undo_file = create_undo_file()
    with open(undo_file, 'r', encoding='utf-8') as f:
        actions = [json.load(f)]

    if not actions[0]:
        print("Нет операций для undo")
        return

    success = execute_undo_action(actions[-1])

    if success:
        actions.pop(-1)

    with open(undo_file, 'w', encoding='utf-8') as f:
        json.dump(actions, f, ensure_ascii=False, indent=2)
