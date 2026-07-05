import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repository import UserRepository
from shared.exceptions import NotFoundError


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def get_profile(self, user_id: str | uuid.UUID) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return {"user": user}

    async def update_profile(self, user_id: str | uuid.UUID, **kwargs) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        updated = await self.repo.update(user, **kwargs)
        return {"user": updated}
