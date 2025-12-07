from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from .routes import auth, health

app = FastAPI(title="resuMAX API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
