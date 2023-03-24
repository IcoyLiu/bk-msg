import requests
import json
from .settings import tencentv3_secret_id, tencentv3_secret_key, tencentv3_templateId, tencentv3_SignName, tencentv3_SmsSdkAppId
from .settings import tencent_sdkapp_id, tencent_app_key, tencent_templateId, tencent_SignName
import hashlib, hmac, json, os, sys, time
from datetime import datetime
import random

# 对应腾讯云3.0 API文档
class Tencentv3:

    # 发送腾讯云短信
    def __init__(self):
        pass

    def send_tententmsg(self, mobile, title, content):
        secret_id = tencent_secret_id
        secret_key = tencent_secret_key
        service = "sms"
        host = "sms.tencentcloudapi.com"
        endpoint = "https://" + host
        region = "ap-guangzhou"
        action = "SendSms"
        version = "2021-01-11"
        algorithm = "TC3-HMAC-SHA256"
        timestamp = int(time.time())
        # timestamp = 1551113065
        date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        mobile = "+86" + mobile
        #title = "\n" + title
        content_list = content.split("\n")
        alarm_object = content_list[0].split(":")[1]
        alarm_content = content_list[1].split(":")[1]
        alarm_time = content_list[3].split(":")[1]
        alarm_type = content_list[4].split(":")[1]
        alarm_biz = content_list[5].split(":")[1]
        alarm_index = content_list[6].split(":")[1]
        alarm_source = content_list[7].split(":")[1]
        alarm_status = content_list[8].split(":")[1]
        params = {
            "PhoneNumberSet": [mobile],
            "SmsSdkAppId": tencent_SmsSdkAppId,
            "TemplateId": tencent_templateId,
            "SignName": tencent_SignName,
            "TemplateParamSet": [alarm_object, alarm_content, alarm_time, alarm_type, alarm_biz, alarm_index, alarm_source, alarm_status, ""]
        }

        # ************* 步骤 1：拼接规范请求串 *************
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        payload = json.dumps(params)
        canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, host, action.lower())
        signed_headers = "content-type;host;x-tc-action"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (http_request_method + "\n" +
                             canonical_uri + "\n" +
                             canonical_querystring + "\n" +
                             canonical_headers + "\n" +
                             signed_headers + "\n" +
                             hashed_request_payload)

        # ************* 步骤 2：拼接待签名字符串 *************
        credential_scope = date + "/" + service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (algorithm + "\n" +
                          str(timestamp) + "\n" +
                          credential_scope + "\n" +
                          hashed_canonical_request)

        # ************* 步骤 3：计算签名 *************
        # 计算签名摘要函数
        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
        secret_service = sign(secret_date, service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

        # ************* 步骤 4：拼接 Authorization *************
        authorization = (algorithm + " " +
                         "Credential=" + secret_id + "/" + credential_scope + ", " +
                         "SignedHeaders=" + signed_headers + ", " +
                         "Signature=" + signature)
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": host,
            "X-TC-Action": action,
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Version": version,
            "X-TC-Region": region
        }
        resp = requests.post(url=endpoint, headers=headers, data=payload)
        return resp.json()["Response"]["SendStatusSet"][0]["Code"]


# 对应腾讯云2.0 API文档
class Tencent:

    # 发送腾讯云短信
    def __init__(self):
        pass

    def send_tententmsg(self, mobile, title, content):
        url = "https://yun.tim.qq.com/v5/tlssmssvr/sendmultisms2"
        sdkappid = tencent_sdkapp_id
        appkey = tencent_app_key
        templateId = tencent_templateId
        signName = tencent_SignName
        timestamp = str(int(time.time()))

        random_num = str(random.randint(0, 100000000))

        sig = "appkey=" + appkey + "&random=" + random_num + "&time=" + timestamp + "&mobile=" + mobile
        sig = sig.encode('utf-8')
        hash_object = hashlib.sha256()
        # 对数据进行哈希计算
        hash_object.update(sig)
        # 获取哈希值
        sig = hash_object.hexdigest()

        content_list = content.split("\n")
        alarm_object = content_list[0].split(":")[1]
        alarm_content = content_list[1].split(":")[1]
        alarm_time = content_list[3][content_list[3].find(':') + 1:]
        alarm_type = content_list[4].split(":")[1]
        alarm_biz = content_list[5].split(":")[1]
        alarm_index = content_list[6].split(":")[1]
        alarm_source = content_list[7].split(":")[1]
        alarm_status = content_list[8].split(":")[1]

        params_content = [alarm_object, alarm_content, alarm_time, alarm_type, alarm_biz, alarm_index, alarm_source,
                          alarm_status, ""]
        params = {
            "sdkappid": sdkappid,
            "random": random_num,
        }
        data = {
            "ext": "",
            "extend": "",
            "params": params_content,
            "sig": sig,
            "sign": signName,
            "tel": [
                {
                    "mobile": mobile,
                    "nationcode": "86"
                }
            ],
            "time": timestamp,
            "tpl_id": templateId
        }
        resp = requests.post(url=url, params=params, data=json.dumps(data))
        return resp.json()
