import uuid
from datetime import datetime

from pydantic import BaseModel


class CartItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    price: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    items: list[CartItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AddItemRequest(BaseModel):
    product_id: uuid.UUID
    quantity: int = 1
    price: float


class UpdateItemRequest(BaseModel):
    quantity: int
