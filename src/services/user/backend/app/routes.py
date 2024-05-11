import aioredis
from fastapi import APIRouter

import env

router = APIRouter()


async def get_redis():
    redis = await aioredis.from_url(
        f"redis://{env.REDIS_HOST}",
        db=env.REDIS_DB_NAME,
        username=env.REDIS_USERNAME,
        password=env.REDIS_PASSWORD
    )
    try:
        yield redis
    except Exception as _:
        await redis.close()
