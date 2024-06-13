import json
import pika
import redis.asyncio as redis

import env
from logger import get_logger


logger = get_logger(__name__)


def fetch_plans():
    credentials = pika.PlainCredentials(
        env.RABBITMQ_USERNAME,
        env.RABBITMQ_PASSWORD
    )

    conn_params = pika.ConnectionParameters(
        host=env.RABBITMQ_HOST,
        credentials=credentials
    )

    with pika.BlockingConnection(conn_params) as conn:
        channel = conn.channel()

        channel.basic_publish(
            exchange="",
            routing_key=env.ADMIN_SERVER_QUEUE,
            body="",
            properties=pika.BasicProperties(
                reply_to=env.ADMIN_CLIENT_QUEUE,
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )

        method_frame, header_frame, body = channel.basic_get(
            env.ADMIN_CLIENT_QUEUE,
            auto_ack=True,
        )

        if method_frame:
            logger.info({
                "method_frame": method_frame,
                "header_frame": header_frame,
                "body": body
            })

            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

            return body

        channel.close()


async def get_plans(_redis: redis.Redis):
    key = "plans"

    plans: bytes | None = await _redis.get(key)
    if plans:
        return json.loads(plans)

    logger.info("Plan data not found, Fetching data from admin service")

    plans: bytes | None = fetch_plans()

    if plans:
        logger.info("Plans saved in redis, For future usage")
        await _redis.set(key, plans, ex=1800)
        return json.loads(plans)

    logger.error("Plans data not found")
    return []
