from typing import Callable
from src import (
    run_ls, run_cd, run_cat, run_cp, run_mv, run_rm, run_zip, run_unzip, run_tar, run_untar,
    run_grep
)

file_commands: dict[str, Callable] = {
    'ls': run_ls,
    'cd': run_cd,
    'cat': run_cat,
    'cp': run_cp,
    'mv': run_mv,
    'rm': run_rm,
    'zip': run_zip,
    'unzip': run_unzip,
    'tar': run_tar,
    'untar': run_untar,
    'grep': run_grep
}
