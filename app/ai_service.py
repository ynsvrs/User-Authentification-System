from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt = "Ты AI ассистент. Отвечай логично и продолжай диалог."


def ask_gemini(messages: list):
    conversation = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            conversation += f"Пользователь: {content}\n"
        else:
            conversation += f"Ассистент: {content}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={"system_instruction": system_prompt},
        contents=conversation
    )

    return response.text