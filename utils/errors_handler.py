from utils.my_logger import logger


def handle_error(type_error: str, cmd: str, *args, need_log: bool = False) -> None:
    errors_dict: dict[str, tuple[str, str]] = {
        'invalid_option': (
            f"{cmd}: {args[0] if args else ''}: Такая опция не поддерживается",
            f"{cmd}: {args[0] if args else ''}: Invalid option"
        ),
        'invalid_amount_options': (
            f"{cmd}: Неправильное количество опций",
            f"{cmd}: Invalid amount of options"
        ),
        'invalid_amount_params': (
            f"{cmd}: Неправильное количество аргументов",
            f"{cmd}: Invalid amount of params"
        ),
        'path_not_found': (
            f"{cmd}: {args[0] if args else ''}: Нет такого пути",
            f"{cmd}: {args[0] if args else ''}: No such file or directory"
        ),
        'command_not_found': (
            f"{cmd}: Такая команда не поддерживается",
            f"{cmd}: Command not found"
        ),
        'need_option_not_found': (
            f"{cmd}: Требуется опция {args[0] if args else ''}",
            f"{cmd}: Need option {args[0] if args else ''}"
        ),
        'already_exists': (
            f"{cmd}: {args[0] if args else ''}: Уже существует",
            f"{cmd}: {args[0] if args else ''}: Already exists"
        )
    }

    try:
        print(errors_dict[type_error][0])
    except KeyError:
        print("Нет такой ошибки")

    if need_log:
        logger.error(errors_dict[type_error][1])
