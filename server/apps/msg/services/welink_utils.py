import requests
import json
from .settings import welink_client_id, welink_client_secret


class WeLink:

    # 发送飞书消息
    def __init__(self):
        pass

    def send_welink(self, access_token, user_id, title, content):
        url = "https://open.welink.huaweicloud.com/api/messages/v2/send"
        headers = {
            "Content-Type": "application/json",
            "x-wlk-Authorization": access_token
        }
        msg_title = {
            "CN": title,
            "EN": ""
        }
        msg_content = {
            "CN": content,
            "EN": ""
        }
        data = {
            "toUserList": [user_id],
            "msgTitle": json.dumps(msg_title),
            "msgContent": json.dumps(msg_content)
        }
        resp = requests.post(url=url, headers=headers, data=json.dumps(data))
        return resp.json()["message"]

    # 获取token
    def get_access_token(self):
        url = "https://open.welink.huaweicloud.com/api/auth/v2/tickets"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "client_id": welink_client_id,
            "client_secret": welink_client_secret
        }
        resp = requests.post(url=url, headers=headers, data=json.dumps(data))
        return resp.json()["access_token"]

    # 根据手机号获取用户id
    def get_userid(self, access_token, mobile):
        url = "https://open.welink.huaweicloud.com/api/auth/v1/userids"
        headers = {
            "Accept-Charset": "UTF-8",
            "Content-Type": "application/json",
            "x-wlk-Authorization": access_token,
            "lang": "zh"
        }
        data = {
            "mobileNumbers": ["+86-" + mobile]
        }
        resp = requests.post(url=url, headers=headers, data=json.dumps(data))
        return resp.json()["data"][0]["userId"]
