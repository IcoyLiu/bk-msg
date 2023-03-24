from pydantic import BaseModel, Field


class FLowTicketModel(BaseModel):
    page: int = Field(1, description="页数")
    page_size: int = Field(10, description="每页个数")


class DingTalkModel(BaseModel):
    mobile: str = Field(description="手机号")
    title: str = Field(description="消息标题")
    content: str = Field(description="消息内容")


class KafkaModel(BaseModel):
    mobile: str = Field(description="手机号")
    title: str = Field(description="消息标题")
    content: str = Field(description="消息内容")


class TencentModel(BaseModel):
    mobile: str = Field(description="手机号")
    title: str = Field(description="消息标题")
    content: str = Field(description="消息内容")


class FeishuModel(BaseModel):
    mobile: str = Field(description="手机号")
    title: str = Field(description="消息标题")
    content: str = Field(description="消息内容")

class RabbitMQModel(BaseModel):
    mobile: str = Field(description="手机号")
    title: str = Field(description="消息标题")
    content: str = Field(description="消息内容")

class WeLinkModel(BaseModel):
    mobile: str = Field(description="手机号")
    title: str = Field(description="消息标题")
    content: str = Field(description="消息内容")
