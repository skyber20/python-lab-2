import os
import oslex
import sys
from src.command_registry import file_commands
from src.commands.command_history import run_history
from src.constants import enum_exceptions
from utils.my_logger import logger


def run_command(cmd: str, inp: list[str]) -> tuple[bool, Exception | None]:
    '''

    :param cmd: команда, введенная юзером
    :param inp: Остальной пользовательский вход
    :return: кортеж, где первый элемент - удачно/неудачно выполненная команда, второй элемент -
    тип ошибки, если она была
    '''
    try:
        file_commands[cmd](inp)
        return True, None
    except KeyError:
        print(f'{cmd}: Такая команда не поддерживается')
        logger.error(f'{cmd}: Такая команда не поддерживается')
        return False, KeyError()
    except enum_exceptions as e:
        print(e)
        logger.error(str(e))
        return False, e
    except Exception as e:
        print("Другая ошибка")
        return False, e


def main() -> None:
    '''
    Точка входа
    :return: ничего
    '''
    while sys.stdin:
        inp = input(f"{os.getcwd()}> ")
        logger.info(inp)
        run_history(inp=inp, show=False)

        if inp == 'exit':
            print("Bye")
            break

        clear_inp = inp.replace("'", '"').replace("\\", "/")
        tokens = oslex.split(clear_inp)

        run_command(tokens[0], tokens[1:])


if __name__ == '__main__':
    '''
    Запуск мейна
    '''
    main()
