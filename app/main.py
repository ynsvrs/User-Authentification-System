from fastapi import FastAPI
from app.users.router import router as users_router
from app.tasks import say_hello

app = FastAPI(title="User Service API")

app.include_router(users_router)

@app.get("/")
async def root():
    return {"status": "API is working yay!!"}

@app.get("/say_hello_now")
async def say_hello_now():
    say_hello.delay()
    return {"status": "Задача say_hello отправлена!"}
