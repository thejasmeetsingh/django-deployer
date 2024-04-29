"""
Backend Application Main EntryPoint
"""

from fastapi import FastAPI, status
from pydantic import BaseModel

from auth import routes as auth_routes


def get_app() -> FastAPI:
    _app = FastAPI()

    _app.title = "Django Deployer"
    _app.description = "Admin Backend"

    prefix = "/api/v1"

    _app.include_router(auth_routes.router, prefix=prefix)

    return _app


app = get_app()


# Health Check Route
class HealthCheck(BaseModel):
    message: str


@app.get("/health-check/", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check():
    return HealthCheck(message="Admin backend is up & running!")
