from typing import Annotated

import aiohttp
from fastapi import Depends, HTTPException
from loguru import logger

from entities import User, Team, Resource
from fastapi import Depends, HTTPException, status
from services.auth import AuthService

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


async def is_admin(user: User = Depends(AuthService.get_current_user)) -> User:
    if user.role != "ADMIN":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed to perform this action", 
        )
    return user

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]

async def has_role(user: CurrentUserDep, roles: list[str]) -> User:
    if user.role not in roles:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed to perform this action",
        )
    return user

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]
TeamMembershipRep = Annotated[Team, Depends(TeamService.get_current_team)]
ResourceDep = Annotated[Resource, Depends(ResourceService.get_resource)]

def authorize(user: CurrentUserDep, resource: ResourceDep, team: TeamMembershipRep) -> bool:
    if user.role == 'ADMIN':
        return True
    if user.id in team.members:
        return True
    if resource.is_public:
        return True
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN, detail = "Access Denied"
    )

AuthorizationRep = Annotated[bool, Depends(authorize)]

