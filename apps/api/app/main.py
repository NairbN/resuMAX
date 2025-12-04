from fastapi import FastAPI

from .routes import health

app = FastAPI(title="resuMAX API")

app.include_router(health.router)
