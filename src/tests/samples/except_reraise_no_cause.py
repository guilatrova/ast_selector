"""
Violation:

Reraise without using 'from'
"""


class MyException(Exception):
    pass


def func():
    try:
        a = 1
    except Exception:
        raise MyException()  # exc is Call + cause is None


def func_two():
    try:
        a = 1
    except MyException as e:
        raise e  # exc is Name
    except Exception:
        raise  # exc is None
