import requests
import json
from .settings import feishu_app_secret, feishu_app_id


class FeiShu:

    # 发送飞书消息
    def __init__(self):
        pass

    def send_feishu(self, app_access_token, user_id, title, content):
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + app_access_token
        }
        msg = json.dumps({"text": title + "\n" + content})
        data = {
            "receive_id": user_id,
            "msg_type": "text",
            "content": msg
        }
        params = {
            "receive_id_type": "open_id"
        }
        resp = requests.post(url=url, headers=headers, params=params, data=json.dumps(data))
        return resp.json()["msg"]

    # 获取token
    def get_app_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "app_id": feishu_app_id,
            "app_secret": feishu_app_secret
        }
        resp = requests.post(url=url, headers=headers, data=json.dumps(data))
        return resp.json()["app_access_token"]

    # 根据手机号获取用户id
    def get_userid(self, app_access_token, mobile):
        url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + app_access_token
        }
        data = {
            "mobiles": [mobile]
        }
        resp = requests.post(url=url, headers=headers, data=json.dumps(data))
        return resp.json()["data"]["user_list"][0]["user_id"]
