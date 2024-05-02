"""
Contains models representing Instance related DB tables
"""

import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Instance(Base):
    """
    Allow admin to add instance type like: t2.micro, t3a.medium etc.
    """

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    modified_at: Mapped[datetime] = mapped_column(nullable=False)

    type: Mapped[str] = mapped_column(sa.String(5), nullable=False)

    plans: Mapped[list["Plan"]] = relationship(
        back_populates="instance",
        cascade="all, delete-orphan"
    )

    __tablename__ = "instances"

    def __str__(self):
        return self.type
