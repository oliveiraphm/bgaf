import os
from dotenv import load_dotenv 
from pathlib import Path

from fastapi import FastAPI
from openai import OpenAI

load_dotenv()

dotenv_path = Path(" .env")
load_dotenv(dotenv_path)

openapi_api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()
openai_client = OpenAI(api_key=openapi_api_key)

@app.get("/")
def root_controller():
    return {"status": "healthy"}

@app.get("/chat")
def chat_controller(prompt: str = "Inspire me"):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    statement = response.choices[0].message.content.strip()
    return {"statement": statement}