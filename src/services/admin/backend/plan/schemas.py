"""
Pydantic Schemas for data validation and DB models type annotations
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, Field

from instance.schemas import Instance
from .models import PlanType


class Plan(BaseModel):
    id: UUID4
    created_at: datetime
    modified_at: datetime
    instance: Instance

    name: PlanType

    class Config:
        from_attributes = True


class PlanCreateRequest(BaseModel):
    name: PlanType
    instance_id: UUID4


class PlanUpdateRequest(BaseModel):
    name: Optional[PlanType] = None
    instance_id: Optional[UUID4] = None


class PlanResponse(BaseModel):
    message: str
    data: Plan | None


class PlanListResponse(BaseModel):
    id: UUID4
    name: PlanType
