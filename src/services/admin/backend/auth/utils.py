import datetime

import jwt

import env


def generate_token(payload: dict, exp: datetime.timedelta) -> str:
    payload.update({"exp": datetime.datetime.now(datetime.UTC) + exp})
    return jwt.encode(payload=payload, key=env.SECRET_KEY, algorithm="HS256")


def get_auth_tokens(payload: dict[str, str]) -> dict[str, str]:
    access_token = generate_token(payload, datetime.timedelta(
        minutes=int(env.ACCESS_TOKEN_EXP_MINUTES)))

    refresh_token = generate_token(payload, datetime.timedelta(
        minutes=int(env.REFRESH_TOKEN_EXP_MINUTES)))

    return {
        "access": access_token,
        "refresh": refresh_token
    }


def get_jwt_payload(token: str) -> dict[str, str] | None:
    try:
        return jwt.decode(jwt=token, key=env.SECRET_KEY,
                          algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.DecodeError) as _:
        return None
