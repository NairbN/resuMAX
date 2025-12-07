from typing import Optional

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    redis = None

from app.config import settings


def get_redis() -> Optional["redis.Redis"]:
    if not settings.redis_url or redis is None:
        return None
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)
