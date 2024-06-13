import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate

from instance.models import Instance
from plan.models import Plan, PlanType
from plan.schemas import PlanCreateRequest, PlanUpdateRequest


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


async def update_plan(session: AsyncSession, plan: Plan, plan_request: PlanUpdateRequest) -> Plan:
    if plan_request.name:
        plan.name = plan_request.name

    if plan_request.instance_id:
        plan.instance_id = plan_request.instance_id

    await session.commit()
    await session.refresh(plan)

    return plan


async def delete_plan(session: AsyncSession, plan_id: uuid.UUID) -> None:
    await session.execute(delete(Plan).where(Plan.id == plan_id))
    await session.commit()


async def delete_plans_by_instance_id(session: AsyncSession, instance_id: uuid.UUID) -> None:
    await session.execute(delete(Plan).where(Plan.instance_id == instance_id))
    await session.commit()


async def get_plans(session: AsyncSession, plan_type: PlanType | None) -> list[Plan]:
    query = select(Plan.id, Plan.name)
    if plan_type:
        query = query.filter_by(name=plan_type)
    return await paginate(session, query.order_by(Plan.created_at.desc()))
