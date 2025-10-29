from typing import Callable
from src import run_ls, run_cd, run_cat, run_cp

file_commands: dict[str, Callable] = {
    'ls': run_ls,
    'cd': run_cd,
    'cat': run_cat,
    'cp': run_cp
}