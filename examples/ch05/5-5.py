import os
from fastapi import FastAPI
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

@app.get("/block")
async def block_server_controller():
    completion = sync_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Explain FastAPI in one sentence."}
        ],        
    )
    return completion.choices[0].message.content

@app.get("/slow")
def slow_text_generator():
    completion = sync_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Explain FastAPI in one sentence."}
        ],        
    )
    return completion.choices[0].message.content

@app.get("/fast")
async def fast_text_generator():
    completion = sync_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Explain FastAPI in one sentence."}
        ],        
    )
    return completion.choices[0].message.content

#uvicorn examples.ch05.5-5:app --reload