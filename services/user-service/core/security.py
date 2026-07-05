from datetime import datetime, timedelta, timezone

import bcrypt

from core.config import settings
from shared.utils.auth_utils import create_token, verify_token


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return create_token({"sub": user_id, "exp": expire})


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    return create_token({"sub": user_id, "exp": expire, "type": "refresh"})


def decode_token(token: str) -> dict | None:
    return verify_token(token)
