from fastapi_utils.inferring_router import InferringRouter

from server.apps.example.api.test_api import test_api

example_api = InferringRouter()
example_api.include_router(test_api, prefix="/test", tags=["测试演示"])
