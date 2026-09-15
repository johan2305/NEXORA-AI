import json

import redis

from backend.core.config import get_settings

settings = get_settings()

NOTIFICATIONS_CHANNEL = "nexora:notifications"

_redis_client = redis.from_url(settings.redis_url)


def publish_notification(organization_id: str, notification: dict) -> None:
    payload = json.dumps({"organization_id": organization_id, "notification": notification})
    _redis_client.publish(NOTIFICATIONS_CHANNEL, payload)