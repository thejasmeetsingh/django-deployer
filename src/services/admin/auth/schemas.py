from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access: str
    refresh: str


class TokenResponse(BaseModel):
    message: str
    data: Token | None
