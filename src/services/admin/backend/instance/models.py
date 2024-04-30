"""
Contains models representing Instance related DB tables
"""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class Instance(Base):
    """
    Allow admin to add instance type like: t2.micro, t3a.medium etc.
    """

    id = sa.Column(sa.UUID, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime)
    modified_at = sa.Column(sa.DateTime)

    type = sa.Column(sa.String)

    plan = relationship("Plan", back_populates="instance")

    __tablename__ = "instances"

    def __str__(self):
        return self.type
