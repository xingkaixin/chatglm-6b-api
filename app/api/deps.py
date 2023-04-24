from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core import config
from app.llm import init_embeddings, init_llm

tokenizer, model = init_llm(config.llm_model)
embeddings_model = init_embeddings(config.embedding_model)

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_tokenizer():
    return tokenizer


def get_llm_model():
    return model


def get_embeddings_model():
    return embeddings_model


def is_valid_user(token: str = Depends(reusable_oauth2)) -> bool:
    if token in config.token:
        return True
    raise HTTPException(
        status_code=400, detail="Token is not valid. Please check your token."
    )
