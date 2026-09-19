from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from decimal import Decimal

class VariantBase(BaseModel):
    sku: str = Field(..., max_length=100)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    price_override: Optional[Decimal] = None

class VariantCreate(VariantBase):
    pass

class VariantUpdate(BaseModel):
    sku: Optional[str] = Field(None, max_length=100)
    attributes: Optional[Dict[str, Any]] = None
    price_override: Optional[Decimal] = None

class VariantResponse(VariantBase):
    id: UUID
    product_id: UUID
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    category_id: UUID
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    base_price: Decimal = Field(..., ge=0)
    is_active: bool = True

class ProductCreate(ProductBase):
    variants: Optional[List[VariantCreate]] = None

class ProductUpdate(BaseModel):
    category_id: Optional[UUID] = None
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    base_price: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None
    # Variants update logic could be complex (add/remove/update), we skip nested updates for simplicity in V1

class ProductResponse(ProductBase):
    id: UUID
    variants: List[VariantResponse] = []
    model_config = ConfigDict(from_attributes=True)
