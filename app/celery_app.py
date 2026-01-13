from celery import Celery
from app.config import RABBITMQ_URL, REDIS_URL

celery_app = Celery(
    "worker",
    broker=RABBITMQ_URL,
    backend=REDIS_URL,
    include=["app.tasks"]  # <<< TO JEST KLUCZ

)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Warsaw",
    enable_utc=True,
)
