from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


class AuthorizationData(BaseModel):
    user_id: int
    resource_id: int
    action: str


authorization_client = ...  # Create authorization client


async def enforce(data: AuthorizationData) -> bool:
    response = await authorization_client.decide(data)
    if response.allowed:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
    )


router = APIRouter(
    dependencies=[Depends(enforce)], prefix="/generate", tags=["Resource"]
)


@router.post("/text")
async def generate_text_controller(): ...