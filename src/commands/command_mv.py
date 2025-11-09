import os
from utils.my_logger import logger
from src.commands.command_undo import save_action


def run_mv(inp: list[str]) -> None:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if len(pathes) < 2:
        logger.error(f"mv: Not 2 paths were introduced")
        print(f"mv: Not 2 paths were introduced")
        return

    if options:
        logger.error(f"mv: {options[0]}: Invalid option")
        print(f"mv: {options[0]}: Invalid option")
        return

    destination = os.path.abspath(pathes[-1])
    k = 0
    dict_for_undo = {
        'command': 'mv',
        'sources': [],
        'destinations': []
    }

    for p in pathes[:-1]:
        source: str = os.path.abspath(p)

        if not os.path.exists(source):
            print("Нет такого пути")
            continue

        if os.path.isdir(destination):
            destination: str = os.path.join(destination, os.path.basename(source))

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
        logger.info(f"OK. command 'mv' is successful complete")
        return
    logger.error("mv: Error")
