from datetime import datetime
from celery_app import celery
from app.redis_client import redis_client


@celery.task(name="app.tasks.say_hello")
def say_hello():
    redis_client.set("last_hello", str(datetime.now()))
    print(f"Привет! Сейчас {datetime.now()}")
