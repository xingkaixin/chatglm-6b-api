import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


def generate_id():
    return f"modelperm-{str(uuid.uuid4().hex[:24])}"


def get_current_timestamp():
    return int(datetime.utcnow().timestamp())


class Permission(BaseModel):
    id: str = Field(default_factory=generate_id)
    object: str = "model_permission"
    created: int = Field(default_factory=get_current_timestamp)
    allow_create_engine: bool = False
    allow_sampling: bool = True
    allow_logprobs: bool = True
    allow_search_indices: bool = False
    allow_view: bool = True
    allow_fine_tuning: bool = False
    organization: str = "*"
    group: str = None
    is_blocking: bool = False


class Model(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=get_current_timestamp)
    owned_by: str = "openai"
    permission: List[Permission] = Field(default_factory=lambda: [Permission()])
    root: str
    parent: str = None


class Models(BaseModel):
    object: str = "list"
    data: List[Model]
