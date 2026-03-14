from typing import Annotated

import aiohttp
from fastapi import Depends, HTTPException
from loguru import logger

import os
from dotenv import load_dotenv 

load_dotenv()

client_id_oauth_github = os.getenv("CLIENT_ID_OAUTH_GITHUB")
client_secret_oauth_github = os.getenv("CLIENT_SECRET_OAUTH_GITHUB")

async def exchange_grant_with_access_token(code: str) -> str:
    try:
        body = {
            "client_id_oauth_github": client_id_oauth_github,
            "client_secret_oauth_github": client_id_oauth_github,
            "code": code, 
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://github.com/login/oauth/access_token",
                json=body,
                headers=headers,
            ) as resp:
                access_token_data = await resp.json()
    except Exception as e:
        logger.warning(f"Failed to fetch the access token. Error: {e}")
        raise HTTPException(
            status_code=503, detail="Failed to fetch access token"
        )
    
    if not access_token_data:
        raise HTTPException(
            status_code = 503, detail="Failed to obtain access token"
        )
    
    return access_token_data.get("access_token", "")

ExchangeCodeTokenDep = Annotated[str, Depends(exchange_grant_with_access_token)]