import pika
import json
import asyncio

from sqlalchemy import select

import env
import logger
from database import SessionLocal
from plan.models import Plan
from instance.models import Instance


logger = logger.get_logger(__name__)


async def get_plan_with_instance():
    async with SessionLocal() as session:
        results = await session.execute(
            select(Plan.name, Instance.type).join(
                Instance,
                Plan.instance_id == Instance.id
            ).order_by(Plan.created_at.desc())
        )

        return results.fetchall()


def on_request(ch, method, props, _):
    logger.info("Request Received")

    results = asyncio.get_event_loop().run_until_complete(get_plan_with_instance())

    results = [{"plan": plan.value, "instance": instance}
               for plan, instance in results]

    ch.basic_publish(
        "",
        routing_key=props.reply_to,
        body=json.dumps(results),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

    logger.info("Response Sent!")


if __name__ == "__main__":
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

        channel.queue_declare(queue=env.SERVER_QUEUE, durable=True)
        channel.queue_declare(queue=env.CLIENT_QUEUE, durable=True)

        channel.confirm_delivery()

        channel.basic_consume(queue=env.SERVER_QUEUE,
                              on_message_callback=on_request)

        try:
            logger.info("RPC Server Started!")
            channel.start_consuming()
        except Exception as _:
            logger.info("RPC server stopped")
            channel.stop_consuming()
            channel.close()
