from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from fastapi import FastAPI

app = FastAPI()


app.state.limiter = Limiter(storage_uri="redis://localhost:6379")
app.add_middleware(SlowAPIMiddleware)