import uuid
import traceback
from typing import Annotated

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, status

import env
from logger import get_logger
from schemas import HealthCheck, DeployRequest, DeployResponse, PlanResponse
from message_queue.client import get_plans as get_cached_plans


app = FastAPI()
app.title = "Django Deployer"
app.description = "User Service"

logger = get_logger(__name__)


async def get_redis():
    r = await redis.Redis(
        host=env.REDIS_HOST,
        username=env.REDIS_USERNAME,
        password=env.REDIS_PASSWORD,
        db=env.REDIS_DB_NAME,
        decode_responses=True
    )
    try:
        yield r
    except Exception as _:
        await r.close()


@app.get("/health-check/", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check():
    return HealthCheck(message="User backend is up & running!")


@app.get(path="/api/v1/plan/", response_model=list[PlanResponse], status_code=status.HTTP_200_OK)
async def get_plans(_redis: Annotated[redis.Redis, Depends(get_redis)]):
    try:
        # Fetch plan data from redis
        plans: list[dict[str, str]] = await get_cached_plans(_redis)

        return [PlanResponse(plan=plan["plan"], instance=plan["instance"]) for plan in plans]

    except Exception as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })

        raise HTTPException(detail="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@app.post(path="/api/v1/deploy/", response_model=DeployResponse, status_code=status.HTTP_200_OK)
async def deploy(deploy_request: DeployRequest, _redis: Annotated[redis.Redis, Depends(get_redis)]):
    try:
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
    
    except Exception as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })

        raise HTTPException(detail="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
