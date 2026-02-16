from fastapi import Body
from loguru import logger

from ch04.schemas import TextModelRequest
from scraper import extract_urls, fetch_all

async def get_urls_content(body: TextModelRequest = Body(...)) -> str:
    urls = extract_urls(body.prompt)
    if urls:
        try:
            urls_content = await fetch_all(urls)
            return urls_content
        except Exception as e:
            logger.warnings(f"Failed to fetch one or several URLs - Error: {e}")
    return ""