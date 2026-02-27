from fastapi import FastAPI
from app.users.router import router as users_router
from app.tasks import say_hello
from app.ai_service import ask_gemini
from app.chat_service import (
    create_chat,
    delete_chat,
    get_chat_history,
    add_message
)

app = FastAPI(title="User Service API")

app.include_router(users_router)


@app.get("/")
async def root():
    return {"status": "API работает!!"}


@app.get("/say_hello_now")
async def say_hello_now():
    say_hello.delay()
    return {"status": "Задача say_hello отправлена!"}

@app.post("/ask")
async def ask(question: str):
    context = """
    Naruto — это знаменитое аниме.
    """
    answer = ask_gemini(question, context)
    return {"answer": answer}


@app.post("/chat/create")
def create():
    chat_id = create_chat()
    return {"chat_id": chat_id}


@app.delete("/chat/{chat_id}")
def delete(chat_id: str):
    delete_chat(chat_id)
    return {"status": "чат удалён"}


@app.get("/chat/{chat_id}")
def history(chat_id: str):
    return {"history": get_chat_history(chat_id)}


@app.post("/chat/{chat_id}/message")
def send_message(chat_id: str, message: str):
    add_message(chat_id, "user", message)
    history = get_chat_history(chat_id)
    answer = ask_gemini(history)
    add_message(chat_id, "assistant", answer)
    return {"answer": answer}