import logging
from constants import file_commands


def main() -> None:
    while True:
        inp: list[str] = input().split()

        if inp[0] == 'exit':
            break

        logging.info(' '.join(inp))

        try:
            file_commands[inp[0]](inp[1:])
        except KeyError:
            logging.error(f"command '{inp[0]}' not found")
            print(f"command '{inp[0]}' not found")


if __name__ == '__main__':
    main()
