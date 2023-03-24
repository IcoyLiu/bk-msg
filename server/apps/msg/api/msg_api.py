from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.bk_api_utils.main import ApiManager
from core.http_schemas.common_response_schema import CommonResponseSchema
from server.apps.msg.forms.msg_model import DingTalkModel, KafkaModel, TencentModel, FeishuModel, RabbitMQModel, \
    WeLinkModel
from server.apps.msg.services.dingding_utils import DingDing
from server.apps.msg.services.kafka_utils import Kafka
from server.apps.msg.services.tencent_utils import Tencent
from server.apps.msg.services.feishu_utils import FeiShu
from server.apps.msg.services.rabbitmq_utils import RabbitMQ
from server.apps.msg.services.welink_utils import WeLink

msg_api = InferringRouter()


@cbv(msg_api)
class Api:
    # 钉钉消息API
    @msg_api.post("/dingtalk", response_model=CommonResponseSchema, name="发送钉钉消息")
    async def dingtalk(
            self,
            data:DingTalkModel = Body(
                None,
                description="发送钉钉消息",
                example={
                    "mobile": "12345678901",
                    "title": "告警标题",
                    "content": "告警内容",
                }
            )
    ) -> CommonResponseSchema:
        dingding = DingDing()
        access_token = dingding.get_token()
        user_id = dingding.get_userid(access_token, data.mobile)
        resp = dingding.send_dingtalk(access_token, user_id, data.title, data.content)
        return CommonResponseSchema(data=resp, message="操作成功", success=True)

    # Kafka推送Json API
    @msg_api.post("/kafkamsg", response_model=CommonResponseSchema, name="发送Kafka消息")
    async def kafkamsg(
            self,
            data:KafkaModel = Body(
                None,
                description="发送kafka数据",
                example={
                    "mobile": "12345678901",
                    "title": "告警标题",
                    "content": "告警内容",
                }
            )
    ) -> CommonResponseSchema:
        kafka = Kafka()
        resp = kafka.send_kafka(data.title, data.content)
        return CommonResponseSchema(data=resp, message="操作成功", success=True)

    # 腾讯云短信 API
    @msg_api.post("/tencentmsg", response_model=CommonResponseSchema, name="发送腾讯云短信")
    async def tencentmsg(
            self,
            data:TencentModel = Body(
                None,
                description="发送腾讯云短信",
                example={
                    "mobile": "12345678901",
                    "title": "告警标题",
                    "content": "告警内容",
                }
            )
    ) -> CommonResponseSchema:
        tencent = Tencent()
        resp = tencent.send_tententmsg(data.mobile, data.title, data.content)
        return CommonResponseSchema(data=resp, message="操作成功", success=True)

    # 飞书消息 API
    @msg_api.post("/feishumsg", response_model=CommonResponseSchema, name="发送飞书消息")
    async def feishumsg(
            self,
            data:FeishuModel = Body(
                None,
                description="发送飞书消息",
                example={
                    "mobile": "12345678901",
                    "title": "告警标题",
                    "content": "告警内容",
                }
            )
    ) -> CommonResponseSchema:
        feishu = FeiShu()
        app_access_token = feishu.get_app_access_token()
        user_id = feishu.get_userid(app_access_token, mobile=data.mobile)
        resp = feishu.send_feishu(app_access_token, user_id, data.title, data.content)
        return CommonResponseSchema(data=resp, message="操作成功", success=True)

    # RabbitMq消息 API
    @msg_api.post("/rabbitmqmsg", response_model=CommonResponseSchema, name="发送RabbitMQ消息")
    async def rabbitmqmsg(
            self,
            data:RabbitMQModel = Body(
                None,
                description="发送RabbitMQ消息",
                example={
                    "mobile": "12345678901",
                    "title": "告警标题",
                    "content": "告警内容",
                }
            )
    ) -> CommonResponseSchema:
        rabbitmq = RabbitMQ()
        resp = rabbitmq.send_rabbitmq(data.title, data.content)
        return CommonResponseSchema(data=resp, message="操作成功", success=True)

    # WeLink消息 API
    @msg_api.post("/welinkmsg", response_model=CommonResponseSchema, name="发送WeLink消息")
    async def welinkmsg(
            self,
            data:WeLinkModel = Body(
                None,
                description="发送WeLink消息",
                example={
                    "mobile": "12345678901",
                    "title": "告警标题",
                    "content": "告警内容",
                }
            )
    ) -> CommonResponseSchema:
        welink = WeLink()
        access_token = welink.get_access_token()
        user_id = welink.get_userid(access_token, mobile=data.mobile)
        resp = welink.send_welink(access_token, user_id, data.title, data.content)
        return CommonResponseSchema(data=resp, message="操作成功", success=True)

