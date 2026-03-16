import asyncio
from typing import Annotated

from fastapi import Depends
from loguru import logger
import re 
from typing import Annotated

from openai import AsyncOpenAI
from pydantic import AfterValidator, BaseModel, validate_call

from fastapi import APIRouter, Depends

router = APIRouter()


guardrail_system_prompt = '...'

class LLMClient:
    def __init__(self, system_prompt: str):
        self.client = AsyncOpenAI()
        self.system_prompt = system_prompt

    async def invoke(self, user_query: str) -> str | None:
        response = await self.client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature = 0,
        )
        return response.choices[0].message.content
    
@validate_call
def check_classification_response(value: str | None) -> str:
    if value is None or not re.match(r"^(allowed|disallowed)$", value):
        raise ValueError("Invalid topical guardrail reponses received")
    return value

ClassificationResponse = Annotated[str | None, AfterValidator(check_classification_response)]

class TopicalGuardResponse(BaseModel):
    classification: ClassificationResponse

async def is_topic_allowed(user_query: str) -> TopicalGuardResponse:
    response = await LLMClient(guardrail_system_prompt).invoke(user_query)
    return TopicalGuardResponse(classification=response)

llm_client = LLMClient()

async def invoke_llm_with_guardrails(user_query: str) -> str:
    topical_guardrail_task = asyncio.create_task(is_topic_allowed(user_query))
    chat_task = asyncio.create_task(llm_client.invoke(user_query))

    while True:
        done, _ = await asyncio.wait(
            [topical_guardrail_task, chat_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        if topical_guardrail_task in done:
            topic_allowed = topical_guardrail_task.result()
            if not topic_allowed:
                chat_task.cancel()
                logger.warning("Topical guardrail triggered")
                return "Sorry, I cam only talk about building GenAI services with FastAPI"
            elif chat_task in done:
                return chat_task.result()
        else:
            await asyncio.sleep(0.1)

@router.post("/text/generate") 
async def generate_text_controller(response: Annotated[str, Depends(invoke_llm_with_guardrails)] ) -> str:
    return response
