import json
import uuid
from app.redis_client import redis_client


def create_chat():
    chat_id = str(uuid.uuid4())
    redis_client.set(f"chat:{chat_id}", json.dumps([]))
    return chat_id


def delete_chat(chat_id: str):
    redis_client.delete(f"chat:{chat_id}")


def get_chat_history(chat_id: str):
    data = redis_client.get(f"chat:{chat_id}")
    if not data:
        return []
    return json.loads(data)


def add_message(chat_id: str, role: str, content: str):
    history = get_chat_history(chat_id)
    history.append({"role": role, "content": content})
    redis_client.set(f"chat:{chat_id}", json.dumps(history))