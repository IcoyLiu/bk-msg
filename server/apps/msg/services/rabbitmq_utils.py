import requests
import json
from .settings import rabbitmq_port, rabbitmq_user, rabbitmq_password, rabbitmq_queue, rabbitmq_vhost, \
    rabbitmq_ip, rabbitmq_routing_key
import pika


class RabbitMQ:

    # 推送json到RabbitMQ
    def __init__(self):
        pass

    def send_rabbitmq(self, title, content):
        msg = title + "\n" + content
        data = {"message": msg}
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmq_ip,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)))
        channel = connection.channel()
        channel.basic_publish(exchange='',
                              routing_key=rabbitmq_routing_key,
                              body=json.dumps(data),
                              properties=pika.BasicProperties(delivery_mode=2))
        channel.close()
        return "ok"
