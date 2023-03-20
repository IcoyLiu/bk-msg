from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps

from core.settings import settings


class ThreadPool(ThreadPoolExecutor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def shutdown(self, *args, **kwargs):
        # 避免使用with触发shutdown导致全局线程池结束.
        pass

    def submit(*args, **kwargs):
        # 支持callback模式
        future = ThreadPoolExecutor.submit(*args, **kwargs)
        fn = kwargs.pop("fn", None) or args[1]
        call_backs = getattr(fn, "_callback", OrderedDict())
        for callback in call_backs.values():
            future.add_done_callback(callback)
        return future


# 全局线程池
thread_pool = ThreadPool(settings.max_thread_num)

THREAD_COUNT_KEY = "THREADPOOL_COUNT_{task_uuid}"  # {"all":10,"finish":1}


def add_callback(call_fn):
    """
    :param call_fn: callback函数
    :return:
    example:

        def A_callback(future):
            print(future.result())
            print("A_callback")

        def B_callback(future):
            print("B_callback")

        @add_callback(A_callback)
        @add_callback(B_callback)
        def task(task_id):
            pass

    """

    def outer(func):
        if not hasattr(func, "_callback"):
            func._callback = OrderedDict()
        func._callback[call_fn.__name__] = call_fn

        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return inner

    return outer


def index_tag(func):
    """先进先出原则:索引标注器,把_index返回给result方便排序"""

    @wraps(func)
    def inner(*args, **kwargs):
        _index = kwargs.pop("_index", None)
        result = func(*args, **kwargs)
        if _index is not None:
            result = (_index, result)
        return result

    return inner


def get_fifo_result(result):
    """先进先出原则:根据_index排序并返回对应result
    params : tuple (_index, result)
    return : result
    """
    return [_result[1] for _result in sorted(result, key=lambda x: x[0])]


def thread_run_task(func, bulk_params, *args):
    """多线程执行任务"""
    data = []
    future_to_data = {thread_pool.submit(func, *args, **params) for index, params in bulk_params}
    for future in as_completed(future_to_data):
        data.append(future.result())
    return data


def fifo_thread_run_task(func, bulk_params, *args):
    """先进先出多线程执行任务"""
    data = []
    future_to_data = {
        thread_pool.submit(func, *args, _index=index, **params) for index, params in enumerate(bulk_params)
    }  # 记录顺序
    for future in as_completed(future_to_data):
        data.append(future.result())
    return get_fifo_result(data)


def decorator_except(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return {"result": True, "data": res, "message": ""}
        except Exception as err:
            return {"result": True, "data": None, "message": err}

    return inner
