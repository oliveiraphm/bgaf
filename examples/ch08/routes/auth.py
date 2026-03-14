from typing import Annotated

from entities import User
from fastapi import APIRouter, Depends
from schemas import TokenOut, UserOut
from services.auth import AuthService

from dependencies.auth import ExchangeCodeTokenDep

import secrets
import os
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv 

load_dotenv()


auth_service = AuthService()
RegisterUserDep = Annotated[User, Depends(auth_service.register_user)]
AuthenticateUserCredDep = Annotated[
    str, Depends(auth_service.authenticate_user_with_credentials)
]
AuthenticateUserTokenDep = Annotated[User, Depends(auth_service.register_user)]
PasswordResetDep = Annotated[None, Depends(auth_service.reset_password)]

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user_controller(new_user: RegisterUserDep) -> UserOut:
    return new_user


@router.post("/token")
async def login_for_access_token_controller(
    access_token: AuthenticateUserCredDep,
) -> TokenOut:
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", dependencies=[Depends(auth_service.logout)])
async def logout_access_token_controller() -> dict:
    return {"message": "Logged out"}


@router.post("reset-password")
async def reset_password_controller(credentials: PasswordResetDep) -> dict:
    return {
        "message": "If an account exists, a password reset link will be sent to the provided email"
    }

client_id_oauth_github = os.getenv("CLIENT_ID_OAUTH_GITHUB")
client_secret_oauth_github = os.getenv("CLIENT_SECRET_OAUTH_GITHUB")

router = APIRouter()

@router.get("/oauth/github/login", status_code=status.HTTP_301_MOVED_PERMANENTLY)
def oauth_github_login_controller(request: Request) -> RedirectResponse:
    state = secrets.token_urlsafe(16)
    redirect_uri = request.url_for("oauth_github_callback_controller")
    response = RedirectResponse(
        url=f"https://github.com/login/oauth/authorize"
        f"?client_id={client_id_oauth_github}"
        f"&scope=user"
        f"&state={state}"
        f"&redirect_url={redirect_uri}"
    )
    csrf_token = secrets.token_urlsafe(16)
    request.session["x-csrf-state-token"] = csrf_token
    return response

def check_csrf_state(request: Request, state: str) -> None:
    if state != request.session.get("x-csrf-token"):
        raise HTTPException(detail="Bad request", status_code=401)
    
@router.get("/oauth/github/callback", dependencies=[Depends(check_csrf_state)])
async def oauth_github_callback_controller(
    access_token: ExchangeCodeTokenDep,
) -> RedirectResponse:
    response = RedirectResponse(url=f"http://localhost:8501")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response