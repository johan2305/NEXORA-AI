import redis

from backend.core.config import get_settings


def test_redis_connection():
    settings = get_settings()
    client = redis.from_url(settings.redis_url)

    assert client.ping() is True

    client.close()