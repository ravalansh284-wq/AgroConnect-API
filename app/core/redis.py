import redis
import os
import json
from dotenv import load_dotenv

r = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def get_cache(key: str):
    try:
        data = r.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"⚠️ Redis Warning (Get): {e}")
        return None
    
def set_cache(key: str, value: dict, expire: int = 3600):
    try:
        r.set(key, json.dumps(value), ex=expire)
    except Exception as e:
        print(f"⚠️ Redis Warning (Set): {e}")