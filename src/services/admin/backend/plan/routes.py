import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db_session, get_user
from .schemas import PlanResponse, PlanListResponse, PlanCreateRequest, PlanUpdateRequest

router = APIRouter()


@router.get(path="/plan/", response_model=Page[PlanListResponse], status_code=status.HTTP_200_OK)
async def get_plans(session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    pass


@router.post(path="/plan/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def add_plan(plan_request: PlanCreateRequest, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    pass


@router.get(path="/plan/{plan_id}/", response_model=PlanResponse, status_code=status.HTTP_200_OK)
async def get_plan_detail(plan_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    pass


@router.patch(path="/plan/{plan_id}/", response_model=PlanResponse, status_code=status.HTTP_200_OK)
async def update_plan(plan_id: uuid.UUID, plan_request: PlanUpdateRequest, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    pass


@router.delete(path="/plan/{plan_id}/", response_model=PlanResponse, status_code=status.HTTP_200_OK)
async def delete_plan(plan_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_db_session)], _: Annotated[str, Depends(get_user)]):
    pass
