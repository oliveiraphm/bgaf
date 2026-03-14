import secrets
import os
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv 

load_dotenv()

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
