import json

from fastapi import APIRouter, status

import env
from .schemas import LoginRequest, TokenResponse, Token
from .utils import check_password, get_auth_tokens

router = APIRouter()


@router.post(
    path="/login/",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def login(login_request: LoginRequest):
    """
    Login API route

    :param login_request: Login request schema instance
    :return: Instance of TokenResponse schema
    """

    admins: list[dict[str, str]] = json.loads(env.ADMIN_CREDENTIALS)

    for admin in admins:
        if login_request.email in admin:
            # Check password is valid or not
            if check_password(login_request.password, admin["password"]):
                # Generate auth tokens
                tokens = get_auth_tokens({"email": login_request.email})

                return TokenResponse(
                    message="Login Successfully!",
                    data=Token(
                        access=tokens["access"],
                        refresh=tokens["refresh"]
                    )
                )

    return TokenResponse(message="Invalid credentials", data=None)
