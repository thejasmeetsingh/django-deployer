"""
Contains models representing Plan related DB tables
"""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class Plan(Base):
    """
    There will only 3 plans in terms of instance configuration:
    L -> Low Spec
    M -> Medium Spec
    H -> High Spec
    """

    id = sa.Column(sa.UUID, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime)
    modified_at = sa.Column(sa.DateTime)

    name = sa.Column(sa.Enum("B", "S", "P"), unique=True)
    instance_id = sa.Column(sa.UUID, sa.ForeignKey("instances.id"))

    instance = relationship("Instance", back_populates="plan")

    __tablename__ = "plans"

    def __str__(self):
        return self.name
