import logging
logger = logging.getLogger('logger')


class InvalidAmountArguments(Exception):
    def __init__(self, command: str):
        super().__init__(f"{command}: Некорректное количество аргументов")


class InvalidOption(Exception):
    def __init__(self, command: str, option: str):
        super().__init__(f"{command}: Опция {option} не поддерживается")


class InvalidAmountOptions(Exception):
    def __init__(self, command: str):
        super().__init__(f"{command}: Некорректное количество опций")


class InvalidAmountPaths(Exception):
    def __init__(self, command: str):
        super().__init__(f"{command}: Некорректное количество путей")


class PathNotExists(Exception):
    def __init__(self, command: str, path: str):
        super().__init__(f"{command}: Пути {path} не существует")


class IsNotDir(Exception):
    def __init__(self, command: str, filename: str):
        super().__init__(f"{command}: {filename} - Не папка")


class IsNotFile(Exception):
    def __init__(self, command: str, dirname: str):
        super().__init__(f"{command}: {dirname} - Не файл")


class AlreadyExists(Exception):
    def __init__(self, command: str, path: str):
        super().__init__(f"{command}: {path} - Путь уже существует")


class EmptyDir(Exception):
    def __init__(self, command: str, dirname: str):
        super().__init__(f"{command}: {dirname} - Папка пуста")
