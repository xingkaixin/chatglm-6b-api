from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health_check", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "OK"}
