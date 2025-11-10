import os
import re
from src import exceptions


def run_grep(inp: list[str]) -> None:
    if len(inp) != 2:
        raise exceptions.InvalidAmountArguments('grep')

    pattern = inp[0]
    search_path = os.path.abspath(inp[1])
    have_r = False
    have_i = False

    for i in inp[2:]:
        if i == '-r':
            have_r = True
        elif i == '-i':
            have_i = True
        else:
            raise exceptions.InvalidOption('grep', i)

    if not os.path.exists(search_path):
        raise exceptions.PathNotExists('grep', os.path.basename(search_path))

    try:
        ignore_case: bool = re.IGNORECASE if have_i else False
        regex = re.compile(pattern, ignore_case)
    except re.error:
        print(f'grep: {pattern} - отстой')
        exceptions.logger.error(f'grep: {pattern} - отстой')
        return

    files_to_search = []

    if os.path.isfile(search_path):
        files_to_search = [search_path]
    else:
        if have_r:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    files_to_search.append(os.path.join(root, file))
        else:
            print(f'grep: Нужна опция -r для поиска внутри директории')
            exceptions.logger.error(f'grep: Нужна опция -r для поиска внутри директории')
            return

    k = 0

    for file_path in files_to_search:
        try:
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                for num, line in enumerate(f, 1):
                    line = line.strip()
                    if regex.search(line):
                        print(f"{os.path.basename(file_path)}:{num}:{line}")
                        k += 1
        except Exception:
            continue

    if not k:
        print(f"Не удалось найти строки, содержащие pattern: {pattern}")
    exceptions.logger.info(f'grep: OK')
