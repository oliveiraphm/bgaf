from typing import Annotated
from pydantic import computed_field, Field
from utils import count_tokens
from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress, PositiveInt
from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4


SupportedModels = Annotated[
    Literal["tinysd", "sd1.5"], "Supported Image Generation Models"
]


class ModelResponse(BaseModel):
    request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    ip: Annotated[str, IPvAnyAddress] | None
    content: Annotated[str | None, Field(min_length=0, max_length=10000)]
    created_at: datetime = datetime.now()

class TextModelResponse(ModelResponse):
    model: SupportedModels
    price: Annotated[float, Field(ge=0, default=0.01)]
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.0)]

    @property
    @computed_field
    def tokens(self) -> int:
        return count_tokens(self.content)

    @property
    @computed_field
    def cost(self) -> float:
        return self.price * self.tokens


response = TextModelResponse(content="FastAPI Generative AI Service", ip=None)
response.model_dump(exclude_none=True)

# {'content': 'FastAPI Generative AI Service',
#  'cost': 0.06,
#  'created_at': datetime.datetime(2024, 3, 7, 20, 42, 38, 729410),
#  'price': 0.01,
#  'request_id': 'a3f18d85dcb442baa887a505ae8d2cd7',
#  'tokens': 6}

response.model_dump_json(exclude_unset=True)
# '{"ip":null,"content":"FastAPI Generative AI Service","tokens":6,"cost":0.06}'