import uuid
import traceback
from typing import Annotated

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page

from dependencies import get_db_session, get_user
from logger import get_logger
from instance.schemas import InstanceRequest, InstanceResponse, InstanceListResponse
from instance.queries import (
    get_instances as get_instances_db,
    get_instance_by_id,
    create_instance,
    update_instance as update_instance_db,
    delete_instance as delete_instance_db
)

router = APIRouter()
logger = get_logger(__name__)


@router.get(path="/instance/", response_model=Page[InstanceListResponse], status_code=status.HTTP_200_OK)
async def get_instances(session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)], search: str = "") -> Page[InstanceListResponse]:
    return await get_instances_db(session, search)


@router.post(path="/instance/", response_model=InstanceResponse, status_code=status.HTTP_201_CREATED)
async def add_instance(instance_request: InstanceRequest, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        instance = await create_instance(session, instance_request)
        return InstanceResponse(message="Instance added successfully", data=instance)

    except exc.IntegrityError as e:
        raise HTTPException(detail="Instance already exists",
                            status_code=status.HTTP_400_BAD_REQUEST) from e

    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })

        raise HTTPException(detail="Error while creating instance",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.get(path="/instance/{instance_id}/", response_model=InstanceResponse, status_code=status.HTTP_200_OK)
async def get_instance_detail(instance_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        instance = await get_instance_by_id(session, instance_id)
        if not instance:
            raise HTTPException(detail="Instance not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        return InstanceResponse(message="Instance Details", data=instance)
    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })
        raise HTTPException(detail="Error while fetching instance details",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.patch(path="/instance/{instance_id}/", response_model=InstanceResponse, status_code=status.HTTP_200_OK)
async def update_instance(instance_id: uuid.UUID, instance_request: InstanceRequest, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        instance = await get_instance_by_id(session, instance_id)
        if not instance:
            raise HTTPException(detail="Instance not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        instance = await update_instance_db(session, instance_id, instance_request)
        return InstanceResponse(message="Instance detail updated successfully", data=instance)

    except exc.IntegrityError as e:
        raise HTTPException(detail="Instance already exists",
                            status_code=status.HTTP_400_BAD_REQUEST) from e

    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })
        raise HTTPException(detail="Error while updating instance details",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.delete(path="/instance/{instance_id}/", response_model=InstanceResponse, status_code=status.HTTP_200_OK)
async def delete_instance(instance_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    try:
        instance = await get_instance_by_id(session, instance_id)
        if not instance:
            raise HTTPException(detail="Instance not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        await delete_instance_db(session, instance_id)
        return InstanceResponse(message="Instance deleted successfully", data=None)
    except exc.SQLAlchemyError as e:
        logger.error({
            "error": e,
            "traceback": traceback.format_exc()
        })
        raise HTTPException(detail="Error while deleting instance details",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
