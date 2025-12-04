from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def healthcheck():
    return {"status": "ok"}
