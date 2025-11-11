from src.exceptions import (
    InvalidAmountArguments,
    InvalidOption,
    InvalidAmountOptions,
    InvalidAmountPaths,
    PathNotExists,
    IsNotDir,
    IsNotFile,
    AlreadyExists,
    EmptyDir
)

enum_exceptions = (
    InvalidAmountArguments,
    InvalidOption,
    InvalidAmountOptions,
    InvalidAmountPaths,
    PathNotExists,
    IsNotDir,
    IsNotFile,
    AlreadyExists,
    EmptyDir
)

SHELL_LOG = 'shell.log'
TRASH_DIR = '.trash'
UNDO_FILE = "undo_commands.json"
HISTORY_FILE = '.history.txt'
MAX_LINES = 20
