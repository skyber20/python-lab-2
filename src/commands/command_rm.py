import os
from datetime import datetime
from utils.my_logger import logger


def create_trash() -> str:
    trash_dir: str = '.trash'
    cur_dir: str = os.path.dirname(__file__)
    abs_trash: str = os.path.abspath(os.path.join(cur_dir, '..', '..', trash_dir))

    if not os.path.exists(abs_trash):
        os.makedirs(abs_trash)

    return abs_trash


def del_file_dir(abs_apth: str, trash_dir: str, is_dir: bool = False) -> str:
    name: str = os.path.basename(abs_apth)
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    name_to_trash: str = f"{timestamp}_{name}"
    path_to_trash: str = os.path.join(trash_dir, name_to_trash)

    os.rename(abs_apth, path_to_trash)
    return path_to_trash


def run_rm(inp: list[str]) -> dict[str, str | bool | os.PathLike] | bool:
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
        return False

    if len(set(options)) > 1:
        logger.error(f"rm: Only one option can be introduced")
        print(f"rm: Only one option can be introduced")
        return False

    if options and options[0] != '-r':
        logger.error(f"rm: {options[0]}: invalid option")
        print(f"rm: {options[0]}: invalid option")
        return False

    trash_dir: str = create_trash()
    flag: bool = False
    k: int = 0

    for p in pathes:
        abs_path: str = os.path.abspath(p)
        if p in ['/', '.', '..'] or abs_path == os.path.abspath('.'):
            s: str = "rm: cannot be deleted '.', '..', '/'"
            print(s)
            continue

        if os.path.exists(abs_path):
            if os.path.isdir(abs_path):
                if options:
                    sure: str = input(f"{p}: y/n ").lower()
                    flag = True
                    if sure == 'y':
                        del_file_dir(abs_path, trash_dir, True)
                        k += 1
                else:
                    s: str = f"rm: cannot remove {p}: Is a directory"
                    print(s)
            elif os.path.isfile(abs_path):
                sure: str = input(f"{p}: y/n ").lower()
                flag = True
                if sure == 'y':
                    del_file_dir(abs_path, trash_dir)
                    k += 1
        else:
            s: str = f"rm: {p}: No such file or directory"
            print(s)

    if flag:
        logger.info(f"OK. command 'mv' is successful complete")
        if k:
            return True
        return True

    logger.error(s)
    return False
