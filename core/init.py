import logging

from core.logger import logger
from core.logger.conf import LOGGER_NAMES, LOGURU_CONFIG
from core.logger.handlers import InterceptHandler
from core.settings import settings
from core.utils.patch import patch_requests


class InitService(object):
    _init = False

    def __call__(self, *args, **kwargs):
        if not self.__class__._init:
            # 初始化日志
            _init_logger()
            # 给requests打补丁
            if settings.enable_requests_log:
                patch_requests()
            self.__class__._init = True


def _init_logger():
    for logger_name in LOGGER_NAMES:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
    logger.configure(**LOGURU_CONFIG)


init_service = InitService()
