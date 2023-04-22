from fastapi import APIRouter

from .endpoints import chat, embeddings, models, utils

api_router = APIRouter(prefix="/v1")

api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(chat.router, prefix="/chat/completions", tags=["chat"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
