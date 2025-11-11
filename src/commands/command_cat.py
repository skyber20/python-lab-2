from pathlib import Path
from src import exceptions


def run_cat(inp: list[str]) -> None:
    options = []
    pathes = []

    for i in inp:
        if i.startswith('-'):
            options.append(i)
        else:
            pathes.append(i)

    if options:
        raise exceptions.InvalidOption('cat', options[0])

    k = 0

    for i in pathes:
        path = Path(i)
        abs_path = path.absolute()

        if not abs_path.exists():
            print(f'Файла {path} не существует')
            continue

        if abs_path.is_dir():
            print(f'{path} - Не текстовый файл')
            continue

        try:
            print(abs_path.read_text(encoding='utf-8'), end='\n\n')
            k += 1
        except UnicodeDecodeError:
            print(f'{path} - Не текстовый файл')
        except PermissionError:
            print(f'{path} - Недостаточно прав')

    if k:
        exceptions.logger.info("cat: OK")
        return
    exceptions.logger.error('ls: Не OK')
