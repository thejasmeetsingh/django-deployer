"""
Pydantic Schemas for data validation and DB models type annotations
"""

from datetime import datetime

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
    name: PlanType | None
    instance_id: UUID4 | None


class PlanResponse(BaseModel):
    message: str
    data: Plan | None


class PlanList(BaseModel):
    name: PlanType


class PlanListResponse(BaseModel):
    results: list[PlanList]
