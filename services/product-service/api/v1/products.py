from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from services.product_service import ProductService
from dependencies.services import get_product_service

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def read_products(
    query: Optional[str] = None,
    skip: int = 0, limit: int = 100,
    product_service: ProductService = Depends(get_product_service)
):
    if query:
        return await product_service.search(query=query, skip=skip, limit=limit)
    return await product_service.get_all(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service)
):
    product = await product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.create(product_in)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    product_service: ProductService = Depends(get_product_service)
):
    product = await product_service.update(product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service)
):
    success = await product_service.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
