import redis.asyncio as redis
from fastapi import APIRouter

import env

router = APIRouter()


async def get_redis():
    r = await redis.from_url(
        f"redis://{env.REDIS_HOST}",
        db=env.REDIS_DB_NAME,
        username=env.REDIS_USERNAME,
        password=env.REDIS_PASSWORD
    )
    try:
        yield r
    except Exception as _:
        await r.close()
