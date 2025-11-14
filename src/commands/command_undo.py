import json
import os
import shutil
from src.constants import UNDO_FILE
from src import exceptions
from utils.my_logger import logger


def create_undo_file() -> str:
    '''
    Создание undo_commands.json в корневой папке проекта, если такового нет для записвания туда последних команд
    rm, mv, cp
    :return: путь до файла undo_commands.json
    '''
    cur_dir = os.path.dirname(__file__)
    abs_undo_file = os.path.abspath(os.path.join(cur_dir, '..', '..', UNDO_FILE))

    if not os.path.exists(abs_undo_file):
        with open(abs_undo_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

    return abs_undo_file


def save_action(inp: dict[str, str | list[str | bool]]) -> None:
    '''
    Сохраняем последнее действие (cp, mv, rm) в undo_commands.json
    :param inp:
    :return:
    '''
    undo_file = create_undo_file()
    with open(undo_file, 'r', encoding='utf-8') as f:
        actions = json.load(f)

    actions.append(inp)

    with open(undo_file, 'w', encoding='utf-8') as f:
        json.dump(actions, f, ensure_ascii=False, indent=2)


def check_exist_paths(sources: list[str], destinations: list[str]) -> bool:
    '''
    Проверяем, все ли destinations и sources существует. если хотя бы 1 нет - undo считается неудачным
    :return:
    '''
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
    '''
    undo для различных типов команд (rm, cp, mv)
    :param inp: Пользовательский ввод
    :return: удачный/неудачный undo?
    '''
    command = inp['command']
    sources = inp['sources']
    destinations = inp['destinations']
    success = check_exist_paths(sources, destinations)

    if not success:
        logger.error("undo: Ошибка с путями")
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

    logger.info("undo: OK")
    return True


def run_undo(inp: list[str]) -> None:
    '''
    Запуск логики undo. Если в success записалось True, то undo успешен и последнюю команду удаляем
    Иначе - не удаляем последнюю команду
    :param inp: Пользовательский ввод
    :return: ничего
    '''
    if inp:
        raise exceptions.InvalidAmountArguments('undo')

    undo_file = create_undo_file()
    with open(undo_file, 'r', encoding='utf-8') as f:
        actions = json.load(f)

    if not actions:
        print("Нет операций для undo")
        logger.info('undo: OK')
        return

    success = execute_undo_action(actions[-1])

    if success:
        actions.pop(-1)

    with open(undo_file, 'w', encoding='utf-8') as f:
        json.dump(actions, f, ensure_ascii=False, indent=2)
