import os
import stat
from datetime import datetime
from src import exceptions
from utils.my_logger import logger


def assign(lines: list[list[str]]) -> None:
    '''
    Функция для красивого вывода юзеру
    :param lines: строки, что нужно красиво вывести на экран
    :return: ничего
    '''
    lens = []
    for line in lines:
        if line[0] == '?':
            lens.append(1)
        else:
            lens.append(len(line[1]))

    max_ln = max(4, max(lens))

    print(f"MODE{' ' * (8 + (max_ln - 4))}SIZE{' ' * 9}DATE   TIME     NAME")
    for line in lines:
        if line[0] == '?':
            print(f"-?????????{' ' * (max_ln + 1)}?{' ' * 12}?{' ' * 6}?  {line[1]}")
        else:
            print(f"{line[0]}{' ' * (max_ln + 2 - len(line[1]))}{line[1]}{' ' * (13 - len(line[2]))}{line[2]}"
                  f"{' ' * (7 - len(line[3]))}{line[3]}  {line[4]}")


def get_time(unix_time: datetime) -> tuple[str, str]:
    '''
    переводим время в нужный формат из unix time
    :param unix_time: время в формате unix
    :return: кортеж из даты и времени
    '''
    date = datetime.strftime(unix_time, '%d %b %Y')
    time = datetime.strftime(unix_time, '%H:%M')
    return date, time


def get_info(abspath: str, file_dir: str) -> list[str]:
    '''
    если была опция -l. Для подробного вывода
    :param abspath: путь файла/папки
    :param file_dir: название папки/файла
    :return: подробная инфа о файле/папке в виде списка
    '''
    try:
        stats = os.stat(os.path.join(abspath, file_dir))
        mode = stat.filemode(stats.st_mode)
        size = stats.st_size
        date, time = get_time(datetime.fromtimestamp(stats.st_mtime))
        name = file_dir
        return list(map(str, [mode, size, date, time, name]))
    except (FileNotFoundError, OSError, PermissionError):
        return ['?', file_dir]


def run_ls(inp: list[str]) -> None:
    '''
    Выводит список файлов и папок в директории. Если с фалом -l, то выводит и подробную инфу
    :param inp: Пользовательский ввод
    :return: ничего
    '''
    options = []
    paths = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            paths.append(i)
    if not paths:
        paths.append(os.getcwd())

    if options:
        if len(set(options)) > 1:
            raise exceptions.InvalidAmountArguments('ls')
        if options[0] != '-l':
            raise exceptions.InvalidOption('ls', options[0])

    k = 0

    for path in paths:
        abspath = path if os.path.isabs(path) else os.path.abspath(path)

        if not os.path.exists(path):
            print(f"{path}: Нет такого пути")
            continue

        if len(paths) > 1:
            print(f"{path}:")

        if not options:
            if os.path.isdir(abspath):
                try:
                    print(os.listdir(abspath))
                    k += 1
                except PermissionError:
                    print(f"{path}: Недостаточно прав")
            else:
                print(os.path.basename(abspath))
                k += 1
        else:
            lines = []
            k += 1

            if os.path.isdir(abspath):
                for file_dir in os.listdir(abspath):
                    info = get_info(abspath, file_dir)
                    lines.append(info)
            else:
                info = get_info(os.path.dirname(abspath), os.path.basename(abspath))
                lines.append(info)
            assign(lines)
            print()

    if k:
        logger.info("ls: OK")
        return
    logger.error('ls: Не OK')
