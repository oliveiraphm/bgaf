from fastapi import APIRouter
from dependencies.auth import is_admin
from fastapi import APIRouter, Depends, HTTPException
from services.auth import AuthService

#router = APIRouter(prefix="/generate", tags=["Resource"])

router = APIRouter(
    dependencies = [Depends(AuthService.get_current_user)],
    prefix="/generate",
    tags=["Resource"],
)

async def has_role(user: CurrentUserDep, roles: list[str]) -> User:
    if user.role not in roles:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed to perform this action",
        )
    return user

@router.get("/text")
def serve_language_model_controller():
    pass

@router.get("/audio")
def serve_text_to_audio_model_controller():
    pass


@router.post("/image", dependencies=[Depends(is_admin)])
async def generate_image_controller():
    pass

@router.post("/text")
async def generate_text_controller():
    pass

@router.post(
    "/image",
    dependencies=[Depends(lambda user: has_role(user, ["ADMIN", "MODERATOR"]))],
)
async def generate_image_controller(): 
    ...


@router.post(
    "/text", dependencies=[Depends(lambda user: has_role(user, ["EDITOR"]))]
)
async def generate_text_controller(): 
    ...