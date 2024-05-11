from pydantic import BaseModel, EmailStr


class DeployRequest(BaseModel):
    email: EmailStr
    plan: str
    instance: str


class DeployResponse(BaseModel):
    message: str
