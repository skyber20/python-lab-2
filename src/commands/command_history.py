import os


def create_history_file() -> str:
    history_file: str = '.history.txt'
    cur_dir: str = os.path.dirname(__file__)
    abs_history: str = os.path.abspath(os.path.join(cur_dir, '..', '..', history_file))

    if not os.path.exists(abs_history):
        with open(abs_history, 'w', encoding='utf-8'):
            pass

    return abs_history


def run_history(n: int = -1, inp: str = '', show: bool = True) -> None:
    abs_history: str = create_history_file()

    if not show:
        with open(abs_history, 'a', encoding='utf-8') as h:
            h.write(inp.strip() + '\n')
    else:
        with open(abs_history, encoding='utf-8') as h:
            lines = h.readlines()
            n = len(lines) if (n == [] or int(n[0]) < 0) else int(n[0])
            for num, line in enumerate(lines[-n:], len(lines) - n + 1):
                print(f"{num}.{line}", end='')
