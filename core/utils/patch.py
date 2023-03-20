import json
import traceback

import requests

from core.logger import logger


def patch_requests():
    """对 requests 库进行猴子补丁"""
    old_request = requests.Session.request  # 备份原始的 request 方法

    def new_request(session, method, url, **kwargs):
        """新的 request 方法"""
        # 记录请求数据
        request_data = {
            "method": method,
            "url": url,
            "headers": dict(kwargs.get("headers", {}) or {}),
            "params": dict(kwargs.get("params", {}) or {}),
            "data": kwargs.get("data", ""),
            "json": kwargs.get("json", ""),
        }
        error = None
        # 发送请求
        try:
            response = old_request(session, method, url, **kwargs)

            try:
                data = response.json()
            except Exception:
                data = response.content.decode("utf8")
            # 记录响应数据
            response_data = {"status_code": response.status_code, "headers": dict(response.headers), "data": data}
        except Exception as e:
            response_data = {
                "exception": repr(e),
                "traceback": traceback.format_exc(),
            }
            response = None
            error = e
        logger.info(json.dumps({"request": request_data, "response": response_data}, indent=4))
        if not response:
            raise error
        return response

    requests.Session.request = new_request  # 将新的 request 方法替换原始的方法
