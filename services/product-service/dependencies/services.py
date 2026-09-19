from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db_session
from repositories.category_repo import CategoryRepository
from repositories.product_repo import ProductRepository
from services.category_service import CategoryService
from services.product_service import ProductService

def get_category_repo(session: AsyncSession = Depends(get_db_session)) -> CategoryRepository:
    return CategoryRepository(session)

def get_product_repo(session: AsyncSession = Depends(get_db_session)) -> ProductRepository:
    return ProductRepository(session)

def get_category_service(repo: CategoryRepository = Depends(get_category_repo)) -> CategoryService:
    return CategoryService(repo)

def get_product_service(repo: ProductRepository = Depends(get_product_repo)) -> ProductService:
    return ProductService(repo)
