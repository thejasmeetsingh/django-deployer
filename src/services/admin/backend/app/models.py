"""
Contains models representing DB tables
"""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class BaseModel(Base):
    """
    This model contains all the base fields
    """

    id = sa.Column(sa.UUID, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime)
    modified_at = sa.Column(sa.DateTime)

    __abstract__ = True


class Instance(BaseModel):
    """
    Allow admin to add instance type like: t2.micro, t3a.medium etc.
    """

    type = sa.Column(sa.String)

    plan = relationship("Plan", back_populates="instance")

    __tablename__ = "instances"

    def __str__(self):
        return self.type


class Plan(BaseModel):
    """
    There will only 3 plans in terms of instance configuration:
    L -> Low Spec
    M -> Medium Spec
    H -> High Spec
    """

    name = sa.Column(sa.Enum("B", "S", "P"), unique=True)
    instance_id = sa.Column(sa.UUID, sa.ForeignKey("instances.id"))

    instance = relationship("Instance", back_populates="plan")

    __tablename__ = "plans"

    def __str__(self):
        return self.name
