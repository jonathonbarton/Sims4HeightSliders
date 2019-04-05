# Python bytecode 3.3 (3230)
# Embedded file name: injector.py
# Compiled at: 2014-09-10 06:55:00
# Size of source mod 2**32: 826 bytes
from functools import wraps
import inspect

def inject(target_function, new_function):

    @wraps(target_function)
    def _inject(*args, **kwargs):
        return new_function(target_function, *args, **kwargs)

    return _inject


def inject_to(target_object, target_function_name):

    def _inject_to(new_function):
        target_function = getattr(target_object, target_function_name)
        setattr(target_object, target_function_name, inject(target_function, new_function))
        return new_function

    return _inject_to


def is_injectable(target_function, new_function):
    target_argspec = inspect.getargspec(target_function)
    new_argspec = inspect.getargspec(new_function)
    return len(target_argspec.args) == len(new_argspec.args) - 1
