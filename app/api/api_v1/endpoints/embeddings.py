from fastapi import APIRouter, Depends, status

from app import schemas
from app.api import deps

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def create_embeddings(
    *, model=Depends(deps.get_embeddings_model), body: schemas.EmbeddingsInput
):
    embeddings = model.encode(body.input)
    embeddings_data = schemas.Response.Embeddings.EmbeddingData(
        embedding=embeddings.tolist()
    )
    return schemas.Response.Embeddings.Embeddings(data=[embeddings_data])
