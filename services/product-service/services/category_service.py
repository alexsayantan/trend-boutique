from typing import List, Optional
from uuid import UUID
from repositories.category_repo import CategoryRepository
from schemas.category import CategoryCreate, CategoryUpdate
from db.models.category import Category
# from shared.exceptions import NotFoundException, BadRequestException

class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return await self.category_repo.get_multi(skip=skip, limit=limit)

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        return await self.category_repo.get(id=category_id)

    async def create(self, category_in: CategoryCreate) -> Category:
        existing = await self.category_repo.get_by_slug(category_in.slug)
        if existing:
            raise ValueError("Category with this slug already exists") # Should use custom exception
        return await self.category_repo.create(obj_in=category_in)

    async def update(self, category_id: UUID, category_in: CategoryUpdate) -> Optional[Category]:
        category = await self.category_repo.get(id=category_id)
        if not category:
            return None
        return await self.category_repo.update(db_obj=category, obj_in=category_in)

    async def delete(self, category_id: UUID) -> bool:
        category = await self.category_repo.delete(id=category_id)
        return category is not None
