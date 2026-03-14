
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from contextlib import asynccontextmanager
from typing import AsyncIterator


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")