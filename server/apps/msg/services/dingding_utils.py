import requests
import json
from .settings import dingding_appkey, dingding_appsecret, dingding_agent_id


class DingDing:

    # 发送钉钉消息
    def __init__(self):
        pass

    def send_dingtalk(self, access_token, user_id, title, content):
        url = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"
        msg = {"msgtype": "text", "text": {"content": title + "\n" + content}}
        data = {
            "agent_id": dingding_agent_id,
            "userid_list": user_id,
            "msg": msg,
        }
        params = {
            "access_token": access_token
        }
        resp = requests.post(url=url, params=params, data=json.dumps(data))
        return resp.json()["errmsg"]

    # 获取token
    def get_token(self):
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": "dingdrvtrc1zzd6wohwf",
            "appsecret": "vTnxW2681P_dmq4P_7OQKwCwRqbTDYehMNITlrEwTJGKFQWkxRgW_C4XiRzs61SI"
        }
        resp = requests.get(url=url, params=params)
        return resp.json()["access_token"]

    # 根据手机号获取用户id
    def get_userid(self, access_token, mobile):
        url = "https://oapi.dingtalk.com/topapi/v2/user/getbymobile"
        data = {
            "mobile": mobile
        }
        params = {
            "access_token": access_token
        }
        resp = requests.post(url=url, params=params, data=json.dumps(data))
        return resp.json()["result"]["userid"]
