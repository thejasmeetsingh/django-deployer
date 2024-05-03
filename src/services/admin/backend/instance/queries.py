import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate

from plan.queries import delete_plans_by_instance_id
from .models import Instance
from .schemas import InstanceRequest


async def get_instance_by_id(session: AsyncSession, instance_id: uuid.UUID) -> Instance:
    _instance = await session.get(Instance, instance_id)
    return _instance


async def create_instance(session: AsyncSession, instance: InstanceRequest) -> Instance:
    _instance = Instance(
        id=uuid.uuid4(),
        type=instance.type
    )

    session.add(_instance)
    await session.commit()

    return _instance


async def update_instance(session: AsyncSession, instance_id: uuid.UUID, instance: InstanceRequest) -> Instance:
    _instance = await get_instance_by_id(session, instance_id)

    _instance.type = instance.type

    await session.commit()
    await session.refresh(_instance)

    return _instance


async def delete_instance(session: AsyncSession, instance_id: uuid.UUID) -> None:
    await session.execute(delete(Instance).where(Instance.id == instance_id))
    await session.commit()

    # Delete related plan objects
    await delete_plans_by_instance_id(session, instance_id)


async def get_instances(session: AsyncSession, search: str) -> list[Instance]:
    return await paginate(session, select(Instance.id, Instance.type).where(Instance.type.like(f"%{search}%")).order_by(Instance.created_at.desc()))
