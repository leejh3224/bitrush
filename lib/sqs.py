import boto3
import os

sqs = boto3.resource("sqs")

order_queue_name = os.getenv("BITRUSH_ORDER_QUEUE_NAME")
order_queue_url = os.getenv("BITRUSH_ORDER_QUEUE_URL")
order_queue = sqs.get_queue_by_name(QueueName=order_queue_name)
