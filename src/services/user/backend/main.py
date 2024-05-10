from fastapi import FastAPI, status
from pydantic import BaseModel


def get_app() -> FastAPI:
    _app = FastAPI()

    _app.title = "Django Deployer"
    _app.description = "User Backend"

    prefix = "/api/v1"

    return _app


app = get_app()

# Health Check Route


class HealthCheck(BaseModel):
    message: str


@app.get("/health-check/", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check():
    return HealthCheck(message="User backend is up & running!")
