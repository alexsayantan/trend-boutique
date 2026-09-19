from typing import List, Optional
from uuid import UUID
from repositories.product_repo import ProductRepository
from schemas.product import ProductCreate, ProductUpdate
from db.models.product import Product

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return await self.product_repo.get_multi(skip=skip, limit=limit)

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return await self.product_repo.get(id=product_id)

    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        return await self.product_repo.search(query=query, skip=skip, limit=limit)

    async def create(self, product_in: ProductCreate) -> Product:
        # In a real scenario, we might want to validate the category exists here
        # or rely on foreign key constraints.
        return await self.product_repo.create(obj_in=product_in)

    async def update(self, product_id: UUID, product_in: ProductUpdate) -> Optional[Product]:
        product = await self.product_repo.get(id=product_id)
        if not product:
            return None
        return await self.product_repo.update(db_obj=product, obj_in=product_in)

    async def delete(self, product_id: UUID) -> bool:
        product = await self.product_repo.delete(id=product_id)
        return product is not None
