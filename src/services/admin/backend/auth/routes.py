import json

from fastapi import APIRouter, status

import env
from .schemas import LoginRequest, TokenResponse, Token, RefreshTokenRequest
from .utils import get_auth_tokens, get_jwt_payload

router = APIRouter()


@router.post(path="/login/", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(login_request: LoginRequest):
    """
    Login API route

    :param login_request: Login request schema instance
    :return: Instance of TokenResponse schema
    """

    admins: list[dict[str, str]] = json.loads(env.ADMIN_CREDENTIALS)

    for admin in admins:
        # Check login credentials are valid or not
        if admin["email"] == login_request.email and admin["password"] == login_request.password:
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


@router.post(path="/refresh-token/", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token_request: RefreshTokenRequest):
    """
    Refresh Token API route

    :param refresh_token_request: Refresh token request schema instance
    :return: Instance of TokenResponse schema
    """

    admins: list[dict[str, str]] = json.loads(env.ADMIN_CREDENTIALS)
    payload: dict[str, str] | None = get_jwt_payload(
        refresh_token_request.refresh_token)

    if payload:
        for admin in admins:
            if payload["email"] == admin["email"]:
                # Generate auth tokens
                tokens = get_auth_tokens(payload)

                return TokenResponse(
                    message="Token Refreshed Successfully!",
                    data=Token(
                        access=tokens["access"],
                        refresh=tokens["refresh"]
                    )
                )

    return TokenResponse(message="Token is invalid or expired", data=None)
