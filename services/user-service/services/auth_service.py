from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from repositories.user_repository import UserRepository
from shared.exceptions import ConflictError, UnauthorizedError


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def signup(self, username: str, email: str, password: str) -> dict:
        existing_user = await self.repo.get_by_username(username)
        if existing_user:
            raise ConflictError("Username already taken")
        existing_email = await self.repo.get_by_email(email)
        if existing_email:
            raise ConflictError("Email already registered")
        user = await self.repo.create(username, email, hash_password(password))
        return {
            "user": user,
            "access_token": create_access_token(str(user.id)),
            "refresh_token": create_refresh_token(str(user.id)),
        }

    async def signin(self, username: str, password: str) -> dict:
        user = await self.repo.get_by_username(username)
        if not user or not verify_password(password, user.password):
            raise UnauthorizedError("Invalid username or password")
        return {
            "user": user,
            "access_token": create_access_token(str(user.id)),
            "refresh_token": create_refresh_token(str(user.id)),
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid or expired refresh token")
        user_id = payload.get("sub")
        return {"access_token": create_access_token(user_id)}
