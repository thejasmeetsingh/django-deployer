"""
Backend Application Main EntryPoint
"""

from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi_pagination import add_pagination

from auth import routes as auth_routes
from instance import routes as instance_routes
from plan import routes as plan_routes


def get_app() -> FastAPI:
    _app = FastAPI()

    _app.title = "Django Deployer"
    _app.description = "Admin Backend"

    prefix = "/api/v1"

    _app.include_router(auth_routes.router, prefix=prefix)
    _app.include_router(instance_routes.router, prefix=prefix)
    _app.include_router(plan_routes.router, prefix=prefix)

    return _app


app = get_app()
add_pagination(app)

# Health Check Route


class HealthCheck(BaseModel):
    message: str


@app.get("/health-check/", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check():
    return HealthCheck(message="Admin backend is up & running!")
