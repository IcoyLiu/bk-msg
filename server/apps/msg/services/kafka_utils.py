import requests
import json
from .settings import kafka_ip, kafka_port, kafka_topic, kafka_key
from kafka import KafkaProducer
from kafka.errors import kafka_errors
import traceback


class Kafka:

    # 推送json到kafka
    def __init__(self):
        pass

    def send_kafka(self, title, content):
        msg = title + "\n" + content
        data = {"message": msg}
        producer = KafkaProducer(
            bootstrap_servers=["{}:{}".format(kafka_ip, kafka_port)],  # kafka服务器ip和端口号
            key_serializer=lambda k: json.dumps(k).encode(),  # 假设生产的消息为json字符串
            value_serializer=lambda v: json.dumps(v).encode())
        future = producer.send(
            kafka_topic,  # 要发送的kafka主题
            key=kafka_key,  # 同一个key值，会被送至同一个分区
            value=data,
            partition=0)  # 向分区1发送消息
        if future.get(timeout=10):
            return "true"
        else:
            return "false"
