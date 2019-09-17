from enum import Enum
import sys

class Colors(Enum):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'


def __print_color(color: Colors, message, *args, **kwargs):
    print(color.value + message + Colors.END.value, *args, **kwargs)


def error(message, *args, **kwargs):
    __print_color(Colors.RED, message, *args, file=sys.stderr, **kwargs)


def warning(message, *args, **kwargs):
    __print_color(Colors.YELLOW, message, *args, **kwargs)


def ok(message, *args, **kwargs):
    __print_color(Colors.GREEN, message, *args, **kwargs)
