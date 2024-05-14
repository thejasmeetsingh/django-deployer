import os
from celery import Celery

from tasks import deploy, send_email


app = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL"),
    backend="rpc://"
)
app.conf.task_default_queue = os.getenv("CELERY_DEFAULT_QUEUE")

app.task(deploy)
app.task(send_email)
