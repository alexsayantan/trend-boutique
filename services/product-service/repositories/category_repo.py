from sqlalchemy.ext.asyncio import AsyncSession
from db.models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from repositories.base import BaseRepository
from sqlalchemy import select
from typing import Optional

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.session.execute(select(Category).filter(Category.slug == slug))
        return result.scalars().first()
