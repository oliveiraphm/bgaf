from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress, PositiveInt


class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min_length=1, max_length=10000)]


class ModelResponse(BaseModel):
    request_id: Annotated[str,Field(default_factory=lambda: uuid4().hex)]
    ip: Annotated[str, IPvAnyAddress] | None = None
    content: Annotated[str | bytes | None, Field(max_length=10000)] = None

    created_at: datetime = Field(default_factory=datetime.now)

class TextModelRequest(ModelRequest):
    model: Literal["gpt-3.5-turbo", "gpt-4o"]
    temperature: Annotated[float,Field(ge=0.0, le=1.0)] = 0.0

class TextModelResponse(ModelResponse):
    tokens: Annotated[int, Field(ge=0)]

ImageSize = Annotated[tuple[PositiveInt, PositiveInt],"Width and height of an image in pixels"]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "sd1.5"]
    output_size: ImageSize
    num_inference_steps: Annotated[int,Field(ge=0, le=2000)] = 200


class ImageModelResponse(ModelResponse):
    size: ImageSize
    url: HttpUrl | None = None