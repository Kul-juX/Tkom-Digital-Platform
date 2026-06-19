from app.core.redis_client import redis_client

BLACKLIST_PREFIX = "blacklist:"


def blacklist_token(token: str):
    if redis_client:
        redis_client.set(BLACKLIST_PREFIX + token, "true")
    return True


def is_token_blacklisted(token: str):
    if redis_client:
        return redis_client.get(BLACKLIST_PREFIX + token) is not None
    return False