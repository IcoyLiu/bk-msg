import json
import json
import os
from urllib.parse import urljoin

import urllib.parse
import requests

from core.exception.base import ClientError
from core.logger import logger
from core.settings import settings
from core.utils.common import combomethod
from core.utils.performance import fn_performance


class SiteConfig(object):
    FLOW = os.getenv("BKAPP_FLOW_SAAS_APP_ID", "bk_itsm")  # 流程管理


class LinkConfig(object):
    config_args_key = "config_args"
    config_kwargs_key = "config_kwargs"

    @combomethod
    def add_config(cls, *args, **kwargs):
        setattr(cls, cls.config_args_key, args)
        setattr(cls, cls.config_kwargs_key, kwargs)
        for k, v in cls.__dict__.items():
            if isinstance(v, (BaseAPIOperation, BKApiDefine)):
                setattr(v, cls.config_args_key, args)
                setattr(v, cls.config_kwargs_key, kwargs)
                v.has_config = True
        setattr(cls, "has_config", True)
        return cls

    def __getattribute__(self, item):
        value = super().__getattribute__(item)
        if not getattr(value, "has_config", False) and isinstance(value, (BaseAPIOperation, BaseApiDefine)):
            value.add_config(*getattr(self, self.config_args_key, ()), **getattr(self, self.config_kwargs_key, {}))
        return value


class BaseApiDefine(LinkConfig):
    HTTP_STATUS_OK_LIST = [200, 201, 204]

    def __init__(self, site, path, method, description="", is_json=True, is_file=False):
        # Do not use join, use '+' because path may starts with '/'
        self.site = site
        self.path = path
        self.method = method
        self.description = description
        self.is_json = is_json
        self.is_file = is_file
        self.headers = {}

    @property
    def total_url(self):
        raise NotImplementedError("需重写获取全url方式的方法")

    def __call__(self, **kwargs):
        if kwargs.get("headers"):
            kwargs["headers"].update(self.headers)
        else:
            kwargs["headers"] = self.headers
        return self._call(**kwargs)

    def http_request(self, total_url, headers, cookies, params, data):
        try:
            if self.is_file:
                files = data.pop("files", None)
                # headers["ContentType"] = "application/x-www-form-urlencoded"
                resp = requests.request(
                    self.method,
                    total_url,
                    headers=headers,
                    cookies=cookies,
                    params=params,
                    files=files,
                    data=data,
                    verify=False,
                )
            else:
                resp = requests.request(
                    self.method, total_url, headers=headers, cookies=cookies, params=params, json=data, verify=False
                )
        except Exception as e:
            raise ClientError(f"请求地址[{total_url}]失败，请求方式[{self.method}]，异常原因[{e}]")
        # Parse result
        if resp.status_code not in self.HTTP_STATUS_OK_LIST:
            err_msg = "请求{}返回异常，请求参数:params【{}】，body【{}】, 状态码: {}".format(total_url, params, data, resp.status_code)
            logger.error(err_msg)
            raise ClientError(err_msg)
        try:
            return resp.json() if self.is_json else resp
        except Exception:
            err_msg = f"""请求参数：params【{params}】，body【{data}】
        失败原因：返回数据无法json化"""
            raise ClientError(err_msg)

    def http_get(self, headers, cookies, params, total_url):
        params = {i: json.dumps(v) if isinstance(v, (dict, list)) else v for i, v in params.items()}
        return self.http_request(total_url, headers, cookies, params, {})

    def http_post(self, headers, cookies, params, total_url):
        data = params
        params = None
        return self.http_request(total_url, headers, cookies, params, data)

    @fn_performance
    def _call(self, **kwargs):
        url_params = kwargs.pop("url_params", {})
        headers = kwargs.pop("headers", {})
        headers.update(self.headers)
        cookies = kwargs.pop("cookies", {})
        params = {}
        params.update(kwargs)
        total_url = self.total_url.format(**url_params)
        http_map = {
            "GET": self.http_get,
            "POST": self.http_post,
            "PUT": self.http_post,
            "PATCH": self.http_post,
            "DELETE": self.http_post,
        }
        fun = http_map.get(self.method, self.http_get)
        return fun(headers, cookies, params, total_url)  # noqa


class BKApiDefine(BaseApiDefine):
    def __init__(self, site, path, method, description="", is_json=True, is_file=False):
        super(BKApiDefine, self).__init__(site, path, method, description=description, is_json=is_json, is_file=is_file)
        host = settings.bk_paas_host
        # Do not use join, use '+' because path may starts with '/'
        self.headers = {"AUTH_APP": "WEOPS"}  # CSRF认证取消
        self.host = host.rstrip("/")

    @property
    def total_url(self):
        if settings.env == "dev":
            env_ = "t"
        else:
            env_ = "o"

        path = f"/{env_}/{self.site}{self.path}"
        return urljoin(self.host, path)


class BaseAPIOperation(LinkConfig):
    def __init__(self):
        # self.get_demo = BKApiDefine(self.SITE, '/test_get/', 'get', description=
        # "查询用户列表")
        self.site = None


class FlowOperation(BaseAPIOperation):
    def __init__(self):
        super().__init__()
        self.site = SiteConfig.FLOW
        self.over_get_tickets = BKApiDefine(self.site, "/openapi/ticket/over_get_tickets/", "GET", description="获取单据")


class DouBanDefine(BaseApiDefine):
    def __init__(self, site, path, method, description="", is_json=True, is_file=False):
        super().__init__(site, path, method, description, is_json, is_file)
        self.headers = {
            "Referer": "https://movie.douban.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

    @property
    def total_url(self):
        return f"https://movie.douban.com/j/{self.path}"

"""
class DouBanHighMovieDefine(BaseApiDefine):
    def __init__(self, site, path, method, description="", is_json=True, is_file=False):
        super().__init__(site, path, method, description, is_json, is_file)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

    @property
    def total_url(self):
        url = "https://movie.douban.com/j/search_subjects/"
        return url
"""


class DouBanOperation(BaseAPIOperation):
    def __init__(self):
        super().__init__()
        self.search_tags = DouBanDefine(self.site, "search_tags", "GET", description="获取标签")


"""
class DouBanHighMovieOperation(BaseAPIOperation):
    def __init__(self):
        super().__init__()
        self.search_movies = DouBanHighMovieDefine(self.site, "search_tags", "GET", description="获取标签")


# 定义腾讯云短信接口
class TencentSMSDefine(BaseApiDefine):
    def __init__(self, site, path, method, description="", is_json=True, is_file=False):
        super().__init__(site, path, method, description, is_json, is_file)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

    @property
    def total_url(self):
        url = "https://movie.douban.com/j/search_subjects/"
        return url

# 定义腾讯云短信行为
class TencentSMSOperation(BaseAPIOperation):
    def __init__(self):
        super().__init__()
        self.search_tags = DouBanDefine(self.site, "search_tags", "GET", description="获取标签")

# 定义钉钉消息接口
class DingDingTalkDefine(BaseApiDefine):
    def __init__(self, site, path, method, description="", is_json=True, is_file=False):
        super().__init__(site, path, method, description, is_json, is_file)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

    @property
    def total_url(self):
        url = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"
        return url

    # 获取token
    def get_token(self):
        data = None
        params = {
            "appkey": "dingdrvtrc1zzd6wohwf",
            "appsecret": "vTnxW2681P_dmq4P_7OQKwCwRqbTDYehMNITlrEwTJGKFQWkxRgW_C4XiRzs61SI"
        }
        token_url = "https://oapi.dingtalk.com/gettoken"
        res = requests.get(url=token_url, params=params, data=json.dumps(data))
        return res.json()["access_token"]

    # 根据手机号获取用户id
    def get_userid(self, access_token, mobile):
        data = {
            "mobile": mobile
        }
        params = {
            "access_token": access_token
        }
        user_url = "https://oapi.dingtalk.com/topapi/v2/user/getbymobile"
        res = requests.post(url=user_url, params=params, data=data)
        logger.error(res.json())
        logger.error(mobile)
        return res.json()["result"]["userid"]

    @fn_performance
    def _call(self, **kwargs):
        access_token = self.get_token()
        url_params = {"access_token": access_token}
        headers = kwargs.pop("headers", {})
        headers.update(self.headers)
        cookies = kwargs.pop("cookies", {})
        mobile = kwargs.pop("mobile", {})
        user_id = self.get_userid(access_token, mobile)
        params = {}
        params.update(kwargs)
        params.append["userid_list"] = user_id
        params.append["agent_id"] = "2480439072"
        total_url = self.total_url.format(**url_params)
        http_map = {
            "GET": self.http_get,
            "POST": self.http_post,
            "PUT": self.http_post,
            "PATCH": self.http_post,
            "DELETE": self.http_post,
        }
        fun = http_map.get(self.method, self.http_get)
        return fun(headers, cookies, params, total_url)  # noqa


# 定义钉钉消息行为
class DingDingTalkOperation(BaseAPIOperation):
    def __init__(self):
        super().__init__()
        self.send_dingtalk = DingDingTalkDefine(self.site, "send_dingtalk", "POST", description="发送钉钉消息")


# 定义Kafka消息接口
class KafkaDefine(BaseApiDefine):
    def __init__(self, site, path, method, description="", is_json=True, is_file=False):
        super().__init__(site, path, method, description, is_json, is_file)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

    @property
    def total_url(self):
        url = "https://movie.douban.com/j/search_subjects/"
        return url

# 定义Kafka消息行为
class KafkaOperation(BaseAPIOperation):
    def __init__(self):
        super().__init__()
        self.search_tags = DouBanDefine(self.site, "search_tags", "GET", description="获取标签")
"""

class ApiManager(LinkConfig):
    flow = FlowOperation()
    douban = DouBanOperation()
    #highMovie = DouBanHighMovieOperation()
    #dingding = DingDingTalkOperation()
