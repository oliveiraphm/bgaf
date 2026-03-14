from fastapi import APIRouter

router = APIRouter(prefix="/generate", tags=["Resource"])

@router.get("/text")
def serve_language_model_controller():
    pass

@router.get("/audio")
def serve_text_to_audio_model_controller():
    pass

from typing import Annotated

import routes
from entities import User
from fastapi import Depends, FastAPI
from services.auth import AuthService
from contextlib import asynccontextmanager
from typing import AsyncIterator

auth_service = AuthService()
AuthenticateUserDep = Annotated[User, Depends(auth_service.get_current_user)]

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routes.auth.router, prefix="/auth", tags=["Auth"])
app.include_router(
    routes.resource.router,
    dependencies=[AuthenticateUserDep],
    prefix="/generate",
    tags=["Generate"],
)
