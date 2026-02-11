import redis
import os
import json
from dotenv import load_dotenv

r = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def get_cache(key: str):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, data: dict, expire: int = 60):
    r.set(key, json.dumps(data), ex=expire)