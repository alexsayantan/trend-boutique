from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from uuid import UUID

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)
    parent_id: Optional[UUID] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    parent_id: Optional[UUID] = None

class CategoryResponse(CategoryBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
