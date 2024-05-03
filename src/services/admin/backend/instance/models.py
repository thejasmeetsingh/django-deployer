"""
Contains models representing Instance related DB tables
"""

import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Instance(Base):
    """
    Allow admin to add instance type like: t2.micro, t3a.medium etc.
    """

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=sa.func.now())
    modified_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=sa.func.now(), server_onupdate=sa.func.now())

    type: Mapped[str] = mapped_column(
        sa.String(50),
        unique=True,
        nullable=False
    )

    __tablename__ = "instances"

    def __str__(self):
        return self.type
