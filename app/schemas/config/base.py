from typing import List, Optional

from pydantic import BaseModel

from ..message import Message


class LLMInput(BaseModel):
    messages: List[Message]
    model: str
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 1
    top_p: Optional[float] = 1.0


class EmbeddingsInput(BaseModel):
    input: str
    model: str
