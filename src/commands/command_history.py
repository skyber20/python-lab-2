import os
from src.constants import MAX_LINES, HISTORY_FILE


def create_history_file() -> str:
    cur_dir = os.path.dirname(__file__)
    abs_history = os.path.abspath(os.path.join(cur_dir, '..', '..', HISTORY_FILE))

    if not os.path.exists(abs_history):
        with open(abs_history, 'w', encoding='utf-8'):
            pass

    return abs_history


def run_history(n: list[str] = [], inp: str = '', show: bool = True) -> None:
    abs_history = create_history_file()

    if not show:
        with open(abs_history, encoding='utf-8') as h:
            try:
                last_line = h.readlines()[-1].strip()
            except IndexError:
                last_line = ''
        if last_line != inp.strip():
            with open(abs_history, 'a', encoding='utf-8') as h:
                h.write(inp.strip() + '\n')
    else:
        with open(abs_history, encoding='utf-8') as h:
            lines = h.readlines()
            if not n or int(n[0]) <= 0:
                n = MAX_LINES
            else:
                n = min(int(n[0]), MAX_LINES)

            for num, line in enumerate(lines[-n:], len(lines) - n + 1):
                print(f"{num}.{line}", end='')
