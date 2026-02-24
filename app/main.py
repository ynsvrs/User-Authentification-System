from fastapi import FastAPI
from app.users.router import router as users_router
from app.tasks import say_hello
from app.ai_service import ask_gemini

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
    Naruto — это знаменитое аниме, созданное на основе манги Масаси Кисимото.
    История рассказывает о мальчике-ниндзя по имени Наруто Узумаки,
    который мечтает стать Хокаге.
    """

    answer = ask_gemini(question, context)

    return {"answer": answer}
