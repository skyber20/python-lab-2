import os
import logging


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
        logging.error("More then 1 option")
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
                    print(path)
            else:
                logging.info(f"OK. command 'ls {' '.join(options)}' is successful complete")
                name: str = os.path.split(abspath)[1]
                size: int = os.path.getsize(abspath)
                # os.path.getmtime()
        else:
            logging.error(f"ls: cannot access {path}: No such file or directory")
            print(f"ls: cannot access {path}: No such file or directory")