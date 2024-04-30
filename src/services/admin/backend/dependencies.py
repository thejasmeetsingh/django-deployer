from fastapi import Request, HTTPException, status

from database import SessionLocal
from auth.utils import get_jwt_payload


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user(request: Request) -> str:
    authorization: str = request.headers.get("authorization")

    if not authorization or "Bearer" not in authorization:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Authentication Required")

    _, access_token = authorization.split()
    payload: dict[str, str] = get_jwt_payload(access_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid token passed")

    admin_email: str | None = payload.get("email")

    if not admin_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Token is invalid or expired")

    return admin_email
