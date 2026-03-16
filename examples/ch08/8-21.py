from typing import Annotated

from entities import User, Team, Resource
from fastapi import Depends, HTTPException, status
from services.auth import AuthService

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

from dependencies.auth import authorize
from fastapi import APIRouter, Depends

router = APIRouter(
    dependencies = [Depends(authorize)], prefix="/generate", tags=["Resource"]
)

@router.post("/image")
async def generate_image_controller():
    pass

@router.post("/text")
async def generate_text_controller():
    pass