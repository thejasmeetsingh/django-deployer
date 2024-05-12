import uuid
from typing import Annotated

import redis.asyncio as redis
from fastapi import FastAPI, Depends, status

import env
from schemas import HealthCheck, DeployRequest, DeployResponse


app = FastAPI()
app.title = "Django Deployer"
app.description = "User Service"


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


@app.get("/health-check/", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check():
    return HealthCheck(message="User backend is up & running!")


@app.post(path="/api/v1/deploy/", response_model=DeployResponse, status_code=status.HTTP_200_OK)
async def deploy(deploy_request: DeployRequest, _redis: Annotated[redis.Redis, Depends(get_redis)]):
    _id = str(uuid.uuid4())
    data = {
        "email": deploy_request.email,
        "plan": deploy_request.plan,
        "instance": deploy_request.instance,
        "is_deployed": False
    }

    # Store deployment data in DB
    await _redis.hset(_id, mapping=data)
    return DeployResponse(message="Deployment request received")
