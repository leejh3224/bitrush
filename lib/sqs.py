import boto3
import os

sqs = boto3.resource("sqs")

order_queue_name = os.getenv("BITRUSH_ORDER_QUEUE")
order_queue = sqs.get_queue_by_name(QueueName=order_queue_name)
