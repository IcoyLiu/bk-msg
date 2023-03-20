import functools
import random
import string


def get_random_pw(length=10):
    words = string.ascii_lowercase + string.ascii_uppercase + string.digits
    chosen = random.sample(words, length)
    return "".join(chosen)


def underline2hump(ul_str: str):
    """下划线转为驼峰"""
    return ul_str.title().replace("_", "")


class combomethod(object):
    def __init__(self, method):
        self.method = method

    def __get__(self, obj=None, objtype=None):
        @functools.wraps(self.method)
        def _wrapper(*args, **kwargs):
            if obj is not None:
                return self.method(obj, *args, **kwargs)
            else:
                return self.method(objtype, *args, **kwargs)

        return _wrapper
