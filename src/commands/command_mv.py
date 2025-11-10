import os
from src.commands.command_undo import save_action
from src import exceptions


def run_mv(inp: list[str]) -> None:
    options = []
    pathes = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if len(pathes) < 2:
        raise exceptions.InvalidAmountPaths('mv')

    if options:
        raise exceptions.InvalidAmountOptions('mw')

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
        exceptions.logger.info(f"mv: OK")
        return
    exceptions.logger.error("mv: Не OK")
