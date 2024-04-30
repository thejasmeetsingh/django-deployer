import uuid
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_db, get_user
from .schemas import InstanceRequest, InstanceResponse, InstanceListResponse

router = APIRouter()


@router.post(path="/instance/", response_model=InstanceResponse, status_code=status.HTTP_201_CREATED)
async def add_instance(instance_request: InstanceRequest, db: Annotated[Session, Depends(get_db)], _: Annotated[Session, Depends(get_user)]):
    pass


@router.get(path="/instance/{instance_id}/", response_model=InstanceResponse, status_code=status.HTTP_200_OK)
async def get_instance_detail(instance_id: uuid.UUID, db: Annotated[Session, Depends(get_db)], _: Annotated[Session, Depends(get_user)]):
    pass


@router.patch(path="/instance/{instance_id}/", response_model=InstanceResponse, status_code=status.HTTP_200_OK)
async def update_instance_detail(instance_request: InstanceRequest, db: Annotated[Session, Depends(get_db)], _: Annotated[Session, Depends(get_user)]):
    pass


@router.delete(path="/instance/{instance_id}/", response_model=InstanceResponse, status_code=status.HTTP_200_OK)
async def delete_instance(instance_id: uuid.UUID, db: Annotated[Session, Depends(get_db)], _: Annotated[Session, Depends(get_user)]):
    pass
