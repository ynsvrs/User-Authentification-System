import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt = "Отвечай на вопросы подробно, смешно и по предоставленному контексту."

def ask_gemini(question: str, context: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": system_prompt
        },
        contents=f"Контекст: {context}\n\nВопрос пользователя: {question}",
    )

    return response.text