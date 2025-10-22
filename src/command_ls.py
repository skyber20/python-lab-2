import os
import stat
import logging
from datetime import datetime


def assign(lines: list[str]) -> None:
    lens: list[int] = []
    for line in lines:
        if line[0] == '?':
            lens.append(1)
        else:
            lens.append(len(line[1]))

    max_ln: int = max(4, max(lens))

    print(f"MODE{' ' * (8 + (max_ln - 4))}SIZE{' ' * 9}DATE   TIME     NAME")
    print()
    for line in lines:
        if line[0] == '?':
            print(f"-?????????{' ' * (max_ln + 1)}?{' ' * 12}?{' ' * 6}?  {line[1]}")
        else:
            print(f"{line[0]}{' ' * (max_ln + 2 - len(line[1]))}{line[1]}{' ' * (13 - len(line[2]))}{line[2]}"
                  f"{' ' * (7 - len(line[3]))}{line[3]}  {line[4]}")
    print()


def get_time(unix_time: datetime):
    date: str = datetime.strftime(unix_time, '%d %b %Y')
    time: str = datetime.strftime(unix_time, '%H:%M')
    return date, time


def get_info(abspath: str) -> list[str]:
    try:
        stats = os.stat(abspath)
        mode: str = stat.filemode(stats.st_mode)
        size: int = stats.st_size
        date, time = get_time(datetime.fromtimestamp(stats.st_mtime))
        name: str = os.path.split(abspath)[1]
        return list(map(str, [mode, size, date, time, name]))
    except (FileNotFoundError, OSError, PermissionError):
        return ['?', os.path.split(abspath)[1]]


def run_ls(inp: list[str | None]=[]) -> None:
    options: list[str] = []
    pathes: list[str] = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)
    if not pathes:
        pathes.append(os.getcwd())

    if len(set(options)) == 1 and options[0] != '-l':
        logging.error(f"Option '{options[0]}' does not exist")
        print(f"Option '{options[0]}' does not exist")
        return
    elif len(set(options)) > 1:
        logging.error("More than 1 option")
        print("More then 1 option")
        return

    for path in pathes:
        abspath: str = path if os.path.isabs(path) else os.path.abspath(path)

        if os.path.exists(abspath):
            if not options:
                logging.info("OK. command 'ls' is successful complete")
                if os.path.isdir(abspath):
                    print(os.listdir(abspath))
                else:
                    print(os.path.split(abspath)[1])
                    # print(path)
            else:
                logging.info(f"OK. command 'ls {' '.join(options)}' is successful complete")
                lines: list[str] = []
                if os.path.isdir(abspath):
                    for file_dir in os.listdir(path):
                        print(os.path.abspath(file_dir))
                        info: list[str] = get_info(os.path.abspath(file_dir))
                        lines.append(info)
                else:
                    info: list[str] = get_info(abspath)
                    lines.append(info)
                assign(lines)
        else:
            logging.error(f"ls: cannot access {path}: No such file or directory")
            print(f"ls: cannot access {path}: No such file or directory")
