from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    # Don't set debug/reload equals True in release, because TimedRotatingFileHandler can't support multi-prcoess
    # please used "uvicorn --host 127.0.0.1 --port 8000 main:app " run in release, and used "python main.py" in dev
    # test   
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=80,
        reload=True,
        log_level="info"
    )
