"""
Pydantic Schemas for data validation and DB models type annotations
"""

from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class Instance(BaseModel):
    id: UUID4
    created_at: datetime
    modified_at: datetime

    type: str

    class Config:
        from_attributes = True


class InstanceRequest(BaseModel):
    type: str = Field(max_length=50)


class InstanceResponse(BaseModel):
    message: str
    data: Instance | None


class InstanceListResponse(BaseModel):
    id: UUID4
    type: str
