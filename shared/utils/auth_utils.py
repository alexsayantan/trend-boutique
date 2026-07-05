from jose import JWTError, jwt

from shared.config import shared_settings


def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            shared_settings.secret_key,
            algorithms=[shared_settings.algorithm],
        )
    except JWTError:
        return None


def create_token(data: dict) -> str:
    return jwt.encode(
        data,
        shared_settings.secret_key,
        algorithm=shared_settings.algorithm,
    )
