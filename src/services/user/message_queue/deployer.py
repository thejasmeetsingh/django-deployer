import env
from celery import Celery


app = Celery(
    __name__,
    broker=f"amqp://{env.RABBITMQ_USERNAME}:{env.RABBITMQ_PASSWORD}@{env.RABBITMQ_HOST}//",
    backend="rpc://"
)
app.conf.task_default_queue = env.CELERY_DEFAULT_QUEUE
