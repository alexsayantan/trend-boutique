from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from services.category_service import CategoryService
from dependencies.services import get_category_service

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
async def read_categories(
    skip: int = 0, limit: int = 100,
    category_service: CategoryService = Depends(get_category_service)
):
    return await category_service.get_all(skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(
    category_id: UUID,
    category_service: CategoryService = Depends(get_category_service)
):
    category = await category_service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        return await category_service.create(category_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service)
):
    category = await category_service.update(category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    category_service: CategoryService = Depends(get_category_service)
):
    success = await category_service.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
