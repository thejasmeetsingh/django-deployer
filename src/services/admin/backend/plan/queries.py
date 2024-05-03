import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate

from .models import Plan
from .schemas import PlanCreateRequest, PlanUpdateRequest


async def get_plan_by_id(session: AsyncSession, plan_id: uuid.UUID) -> Plan:
    _plan = await session.get(Plan, plan_id)
    return _plan


async def create_plan(session: AsyncSession, plan: PlanCreateRequest) -> Plan:
    _plan = Plan(
        id=uuid.uuid4(),
        name=plan.name,
        instance_id=plan.instance_id,
    )

    session.add(_plan)
    await session.commit()

    return _plan


async def update_plan(session: AsyncSession, plan_id: uuid.UUID, plan: PlanUpdateRequest) -> Plan:
    _plan = await get_plan_by_id(session, plan_id)

    if plan.name:
        _plan.name = plan.name

    if plan.instance_id:
        _plan.instance_id = plan.instance_id

    await session.commit()
    await session.refresh(_plan)

    return _plan


async def delete_plan(session: AsyncSession, plan_id: uuid.UUID) -> None:
    await session.execute(delete(Plan).where(Plan.id == plan_id))
    await session.commit()


async def delete_plans_by_instance_id(session: AsyncSession, instance_id: uuid.UUID) -> None:
    await session.execute(delete(Plan).where(Plan.instance_id == instance_id))
    await session.commit()


async def get_plans(session: AsyncSession, search: str) -> list[Plan]:
    return await paginate(session, select(Plan.id, Plan.name).where(Plan.name.like(f"%{search}%")).order_by(Plan.created_at.desc()))
