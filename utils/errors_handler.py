from utils.my_logger import logger


def handle_error(type_error: str, cmd: str, *args, need_log: bool = False) -> None:
    errors_dict: dict[str, tuple[str, str]] = {
        'invalid_option': (
            f"{cmd}: {args[0]}: Такая опция не поддерживается",
            f"{cmd}: {args[0]}: Invalid option"
        )
    }

    try:
        print(errors_dict[type_error][0])
    except KeyError:
        print("Нет такой ошибки")

    if need_log:
        logger.error(errors_dict[type_error][1])
