"""
Pydantic Schemas for data validation and DB models type annotations
"""

from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class Plan(BaseModel):
    id: UUID4
    created_at: datetime
    modified_at: datetime

    name: str

    class Config:
        from_attributes = True


class PlanCreateRequest(BaseModel):
    name: str = Field(max_length=5)
    instance_id: UUID4


class PlanUpdateRequest(BaseModel):
    name: str = Field(max_length=5)


class PlanResponse(BaseModel):
    message: str
    data: Plan


class PlanListResponse(BaseModel):
    results: list[Plan]
