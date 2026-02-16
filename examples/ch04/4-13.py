from dataclasses import dataclass
from typing import Literal

@dataclass
class TextModelRequest:
    model: Literal["tinyLlama", "gemma2b"]
    prompt: str
    temperature: float

@dataclass
class TextModelResponse:
    response: str
    tokens: int


#main.py
from fastapi import Body, FastAPI, HTTPException, status
from ch03.models import generate_text, load_text_model, load_image_model 
from schemas import TextModelRequest, TextModelResponse
from utils import count_tokens
from contextlib import asynccontextmanager
from typing import AsyncIterator

models: dict[str, object] = {}

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    models["text2image"] = load_image_model()
    yield
    models.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/generate/text")
def serve_text_to_text_controller(
    body: TextModelRequest = Body(...),
) -> TextModelResponse:
    if body.model not in ["tinyLlama", "gemma2b"]:
        raise HTTPException(
            detail=f"Model {body.model} is not supported",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    output = generate_text(models["text"], body.prompt, body.temperature)
    tokens = count_tokens(body.prompt) + count_tokens(output)
    return TextModelResponse(response=output, tokens=tokens)