from pydantic import BaseModel, EmailStr


class DeployRequest(BaseModel):
    email: EmailStr
    plan: str
    instance: str


class HealthCheck(BaseModel):
    message: str


class DeployResponse(BaseModel):
    message: str


class PlanResponse(BaseModel):
    plan: str
    instance: str
