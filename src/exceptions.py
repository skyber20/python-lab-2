class InvalidAmountArguments(Exception):
    '''
    Некорректное количество аргументов
    '''
    def __init__(self, command: str):
        super().__init__(f"{command}: Некорректное количество аргументов")


class InvalidOption(Exception):
    '''
    Опция не поддерживается такой то командой
    '''
    def __init__(self, command: str, option: str):
        super().__init__(f"{command}: Опция {option} не поддерживается")


class InvalidAmountOptions(Exception):
    '''
    Некорректное количество опций
    '''
    def __init__(self, command: str):
        super().__init__(f"{command}: Некорректное количество опций")


class InvalidAmountPaths(Exception):
    '''
    Некорректное количество путей
    '''
    def __init__(self, command: str):
        super().__init__(f"{command}: Некорректное количество путей")


class PathNotExists(Exception):
    '''
    Пути не существует
    '''
    def __init__(self, command: str, path: str):
        super().__init__(f"{command}: Пути {path} не существует")


class IsNotDir(Exception):
    '''
    Это не папка
    '''
    def __init__(self, command: str, filename: str):
        super().__init__(f"{command}: {filename} - Не папка")


class IsNotFile(Exception):
    '''
    Это не файл
    '''
    def __init__(self, command: str, dirname: str):
        super().__init__(f"{command}: {dirname} - Не файл")


class AlreadyExists(Exception):
    '''
    Уже такая папка/файл существует
    '''
    def __init__(self, command: str, path: str):
        super().__init__(f"{command}: {path} - Путь уже существует")


class EmptyDir(Exception):
    '''
    Пустая папка
    '''
    def __init__(self, command: str, dirname: str):
        super().__init__(f"{command}: {dirname} - Папка пуста")
