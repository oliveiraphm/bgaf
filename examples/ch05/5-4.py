import os
from fastapi import FastAPI, Body
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv 
from pathlib import Path

load_dotenv()

dotenv_path = Path(" .env")
load_dotenv(dotenv_path)

openapi_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

sync_client = OpenAI(api_key=openapi_api_key)
async_client = AsyncOpenAI(api_key=openapi_api_key)

@app.post("/sync")
def sync_generate_text(prompt: str = Body(...)):
    completion = sync_client.chat.completions.create(
        messages = [
            {
                "role" : "user",
                "content" : prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return completion.choices[0].message.content

@app.post("/async")
async def async_generate_text(prompt: str = Body(...)):
    completion = await async_client.chat.completions.create(
        messages = [
            {
                "role" : "user",
                "content" : prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return completion.choices[0].message.content

#uvicorn examples.ch05.5-4:app --reload