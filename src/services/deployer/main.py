import os
from celery import Celery


app = Celery(__name__, broker=os.getenv("CELERY_BROKER_URL"), backend="rpc://")
app.conf.task_default_queue = os.getenv("CELERY_DEFAULT_QUEUE")
