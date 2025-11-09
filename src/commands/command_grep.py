import os
import re


def run_grep(inp: list[str]) -> None:
    if len(inp) != 2:
        print("Требуется 2 аргумента")
        return

    pattern: str = inp[0]
    search_path: str = os.path.abspath(inp[1])
    have_r: bool = False
    have_i: bool = False

    for i in inp[2:]:
        if i == '-r':
            have_r = True
        elif i == '-i':
            have_i = True
        else:
            print(f"{i}: Неизвестная опция")
            return

    if not os.path.exists(search_path):
        print(f"{inp[1]}: Такого пути не существует")
        return

    try:
        ignore_case: bool = re.IGNORECASE if have_i else False
        regex = re.compile(pattern, ignore_case)
    except re.error as e:
        print(f"{pattern}: invalid pattern")
        return

    files_to_search: list[str] = []

    if os.path.isfile(search_path):
        files_to_search = [search_path]
    else:
        if have_r:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    files_to_search.append(os.path.join(root, file))
        else:
            print("Нужна опция -r")
            return

    flag: bool = False

    for file_path in files_to_search:
        try:
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                for num, line in enumerate(f, 1):
                    line = line.strip()
                    if regex.search(line):
                        print(f"{os.path.basename(file_path)}:{num}:{line}")
                        flag = True
        except Exception as e:
            print("1", e)

    if not flag:
        print(f"Не удалось найти строки, содержащие pattern: {pattern}")
