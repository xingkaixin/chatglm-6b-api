from fastapi import APIRouter, Depends, status

from app import schemas
from app.api import deps

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def list_models(valid_user: bool = Depends(deps.is_valid_user)):
    models_name = [
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo",
        "text-davinci-003",
        "text-embedding-ada-002",
    ]
    models = [
        schemas.Response.Model(id=model_name, root=model_name)
        for model_name in models_name
    ]
    return schemas.Response.Models(data=models)
