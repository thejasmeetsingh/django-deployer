"""
Contains models representing Plan related DB tables
"""

import uuid
from enum import Enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class PlanType(Enum):
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"


class Plan(Base):
    """
    There will only 3 plans in terms of instance configuration:
    L -> Low Spec
    M -> Medium Spec
    H -> High Spec
    """

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=sa.func.now())
    modified_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=sa.func.now(), server_onupdate=sa.func.now())

    name: Mapped[PlanType] = mapped_column(unique=True, nullable=False)
    instance_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("instances.id"),
        nullable=False
    )

    __tablename__ = "plans"

    def __str__(self):
        return self.name
