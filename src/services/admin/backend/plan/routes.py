import uuid
import traceback
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc

from logger import get_logger
from dependencies import get_db_session, get_user
from instance.queries import get_instance_by_id
from plan.models import PlanType
from plan.schemas import PlanResponse, PlanListResponse, PlanCreateRequest, PlanUpdateRequest
from plan.queries import (
    get_plans as get_plans_db,
    get_plan_by_id,
    create_plan,
    update_plan as update_plan_db,
    delete_plan as delete_plan_db
)

router = APIRouter()
logger = get_logger(__name__)


@router.get(path="/plan/", response_model=Page[PlanListResponse], status_code=status.HTTP_200_OK)
async def get_plans(session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)], plan_type: PlanType | None = None):
    return await get_plans_db(session, plan_type)


@router.post(path="/plan/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def add_plan(plan_request: PlanCreateRequest, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        _instance = await get_instance_by_id(session, plan_request.instance_id)
        if not _instance:
            raise HTTPException(detail="Invalid instance ID",
                                status_code=status.HTTP_400_BAD_REQUEST)

        _plan = await create_plan(session, plan_request)
        setattr(_plan, "instance", _instance)

        return PlanResponse(message="Plan added successfully", data=_plan)

    except exc.IntegrityError as e:
        raise HTTPException(detail="Plan already exists",
                            status_code=status.HTTP_400_BAD_REQUEST) from e

    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })

        raise HTTPException(detail="Error while creating plan",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.get(path="/plan/{plan_id}/", response_model=PlanResponse, status_code=status.HTTP_200_OK)
async def get_plan_detail(plan_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        _plan = await get_plan_by_id(session, plan_id)
        if not _plan:
            raise HTTPException(detail="Plan not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        _instance = await get_instance_by_id(session, _plan.instance_id)
        setattr(_plan, "instance", _instance)

        return PlanResponse(message="Plan details", data=_plan)

    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })

        raise HTTPException(detail="Error while fetching plan detail",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.patch(path="/plan/{plan_id}/", response_model=PlanResponse, status_code=status.HTTP_200_OK)
async def update_plan(plan_id: uuid.UUID, plan_request: PlanUpdateRequest, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        _plan = await get_plan_by_id(session, plan_id)
        if not _plan:
            raise HTTPException(detail="Plan not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        _instance = None

        if plan_request.instance_id:
            _instance = await get_instance_by_id(session, plan_request.instance_id)
            if not _instance:
                raise HTTPException(detail="Invalid instance ID",
                                    status_code=status.HTTP_404_NOT_FOUND)

        _plan = await update_plan_db(session, _plan, plan_request)

        if not _instance:
            _instance = await get_instance_by_id(session, _plan.instance_id)

        setattr(_plan, "instance", _instance)

        return PlanResponse(message="Plan details updated successfully", data=_plan)

    except exc.IntegrityError as e:
        print(e)
        raise HTTPException(detail="Plan already exists",
                            status_code=status.HTTP_400_BAD_REQUEST) from e

    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })

        raise HTTPException(detail="Error while updating plan detail",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.delete(path="/plan/{plan_id}/", response_model=PlanResponse, status_code=status.HTTP_200_OK)
async def delete_plan(plan_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        _plan = await get_plan_by_id(session, plan_id)
        if not _plan:
            raise HTTPException(detail="Plan not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        await delete_plan_db(session, plan_id)

        return PlanResponse(message="Plan deleted successfully", data=None)

    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })

        raise HTTPException(detail="Error while deleting plan detail",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
