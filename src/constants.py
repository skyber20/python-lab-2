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
TRASH_DIR = '.trash'
UNDO_FILE = "undo_commands.json"
MAX_LINES = 20
