import json
import pika
import redis.asyncio as redis

import env
from logger import get_logger


REDIS_CONN: redis.Redis | None = None
logger = get_logger(__name__)


async def on_response(ch, _, __, body):
    logger.info("Response: %s", body)

    global REDIS_CONN
    plans: list[dict[str, str]] = json.loads(body)

    logger.info("Saved plans in redis for future use")
    await REDIS_CONN.set("plans", plans, ex=1800)
    await get_plans(REDIS_CONN)

    ch.close()


async def fetch_plans():
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

        channel.basic_consume(
            env.ADMIN_CLIENT_QUEUE,
            auto_ack=True,
            on_message_callback=await on_response
        )

        channel.basic_publish(
            exchange="",
            routing_key=env.ADMIN_SERVER_QUEUE,
            body="",
            properties=pika.BasicProperties(
                reply_to=env.ADMIN_CLIENT_QUEUE,
                delivery_mode=pika.DeliveryMode.Persistent
                )
        )

        channel.start_consuming()


async def get_plans(_redis: redis.Redis):
    plans: list[dict[str, str]] | None = await _redis.get("plans")
    if plans:
        return plans

    logger.info("Plan data not found, Fetching data from admin service")
    global REDIS_CONN
    REDIS_CONN = _redis

    await fetch_plans()
