from fastapi_utils.inferring_router import InferringRouter

#from server.apps.example.api.test_api import test_api
from server.apps.msg.api.msg_api import msg_api

api = InferringRouter()
api.include_router(msg_api, prefix="/msg", tags=["消息推送接口"])
