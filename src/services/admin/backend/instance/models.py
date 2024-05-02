"""
Contains models representing Instance related DB tables
"""

import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Instance(Base):
    """
    Allow admin to add instance type like: t2.micro, t3a.medium etc.
    """

    Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    modified_at: Mapped[datetime] = mapped_column(nullable=False)

    type: Mapped[str] = mapped_column(nullable=False)

    plan = relationship("Plan", back_populates="instance")

    __tablename__ = "instances"

    def __str__(self):
        return self.type
