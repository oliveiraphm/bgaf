from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

app = FastAPI()

limiter = Limiter(
    key_func = get_remote_address,
    default_limits = ["200 per day", "60 per hour", "2/5seconds"],
)

app.state.limiter = limiter

@app.post("/generate/text")
@limiter.limit("5/minute")
def serve_text_to_text_controller(request: Request):
    return ...

@app.post("/generate/image")
@limiter.limit("1/minute")
def serve_text_to_image_controller(request: Request):
    return ...


@app.get("/health")
@limiter.exempt
def check_health_controller(request: Request):
    return {"status": "healthy"}

#9-9.py
@app.post("/generate/text")
@limiter.limit("10/minute", key_func=get_current_user)
def serve_text_to_text_controller(request: Request):
    return {"message": f"Hello User"}