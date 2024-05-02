import uuid
import datetime

from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from .models import Instance
from .schemas import InstanceRequest


def get_instance_by_id(db: Session, instance_id: uuid.UUID) -> Instance:
    return db.get(Instance, instance_id)


def create_instance(db: Session, instance: InstanceRequest) -> Instance:
    _instance = Instance(
        id=uuid.uuid4(),
        created_at=datetime.datetime.now(datetime.UTC),
        modified_at=datetime.datetime.now(datetime.UTC),
        type=instance.type
    )

    db.add(_instance)
    db.commit()

    return _instance


def update_instance(db: Session, instance_id: uuid.UUID, instance: InstanceRequest) -> Instance:
    _instance = get_instance_by_id(db, instance_id)

    db.execute(update(Instance).where(Instance.id == instance_id).values(
        type=instance.type,
        modified_at=datetime.datetime.now(datetime.UTC)
    ))

    db.commit()
    db.refresh(_instance)

    return _instance


def delete_instance(db: Session, instance_id: uuid.UUID) -> None:
    db.execute(delete(Instance).where(Instance.id == instance_id))
    db.commit()


def get_instances(db: Session) -> list[Instance]:
    return paginate(db, select(Instance.id, Instance.type).order_by(Instance.created_at.desc()))
