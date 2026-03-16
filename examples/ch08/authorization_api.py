from typing import Annotated

from entities import User, Team, Resource
from fastapi import FastAPI, Depends, HTTPException, status
from services.auth import AuthService
from pydantic import BaseModel

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]
TeamMembershipRep = Annotated[Team, Depends(TeamService.get_current_team)]
ResourceDep = Annotated[Resource, Depends(ResourceService.get_resource)]

class AuthorizationResponse(BaseModel):
    allowed: bool

app = FastAPI()

app.get("/authorize")

def authorization_controller(user: CurrentUserDep, resource: ResourceDep, action: ActionDep) -> AuthorizationResponse:
    if user.role == 'ADMIN':
        return AuthorizationResponse(allowed=True)
    if action in user.permissions.get(resource.id, []):
        return AuthorizationResponse(allowed=True)
    return AuthorizationResponse(allowed=False)