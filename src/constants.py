from typing import Callable
from src import run_ls, run_cd

file_commands: dict[str, Callable] = {
    'ls': run_ls,
    'cd': run_cd
}