from pydantic import BaseModel, EmailStr, HttpUrl


class DeployRequest(BaseModel):
    email: EmailStr
    plan: str
    instance: str
    repo_link: HttpUrl


class HealthCheck(BaseModel):
    message: str


class DeployResponse(BaseModel):
    message: str


class PlanResponse(BaseModel):
    plan: str
    instance: str
