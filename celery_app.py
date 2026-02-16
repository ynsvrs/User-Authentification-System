from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "user_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.timezone = "Asia/Almaty"

celery.conf.beat_schedule = {
    "say-hello-every-day": {
        "task": "app.tasks.say_hello",
        "schedule": crontab(hour=9, minute=0),
    },
}
import app.tasks
