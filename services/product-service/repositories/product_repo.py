from sqlalchemy.ext.asyncio import AsyncSession
from db.models.product import Product
from db.models.variant import ProductVariant
from schemas.product import ProductCreate, ProductUpdate
from repositories.base import BaseRepository
from sqlalchemy import select
from typing import Optional, List

class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        # Using pg_trgm similarity operator '%' or basic ilike depending on setup.
        # Since pg_trgm is requested, we can use a GIN index on title and description.
        # For simplicity in this implementation, we use ilike which benefits from pg_trgm gin_trgm_ops.
        # If strict similarity is needed: Product.title.bool_op('%')(query)
        search_query = f"%{query}%"
        stmt = select(Product).filter(
            (Product.title.ilike(search_query)) | 
            (Product.description.ilike(search_query))
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
