from fastapi import APIRouter, Depends

from dependencies.cart_dependency import get_cart_service, get_current_user_id
from schemas.cart import AddItemRequest, CartItemResponse, CartResponse, UpdateItemRequest
from services.cart_service import CartService
from shared.schemas.response_schema import UnifiedResponse, success_response

router = APIRouter(tags=["cart"])


@router.get("/me", response_model=UnifiedResponse)
async def get_cart(
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    result = await cart_service.get_or_create_cart(user_id)
    return success_response(
        data=CartResponse.model_validate(result["cart"]).model_dump(),
        message="Cart retrieved successfully",
    )


@router.post("/me/items", response_model=UnifiedResponse, status_code=201)
async def add_item(
    payload: AddItemRequest,
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    result = await cart_service.add_item(
        user_id, payload.product_id, payload.quantity, payload.price
    )
    return success_response(
        data=CartItemResponse.model_validate(result["item"]).model_dump(),
        message="Item added to cart",
    )


@router.patch("/me/items/{item_id}", response_model=UnifiedResponse)
async def update_item(
    item_id: str,
    payload: UpdateItemRequest,
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    result = await cart_service.update_item(user_id, item_id, payload.quantity)
    return success_response(
        data=CartItemResponse.model_validate(result["item"]).model_dump(),
        message="Cart item updated",
    )


@router.delete("/me/items/{item_id}", response_model=UnifiedResponse)
async def remove_item(
    item_id: str,
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    result = await cart_service.remove_item(user_id, item_id)
    return success_response(data=result, message="Item removed from cart")


@router.delete("/me", response_model=UnifiedResponse)
async def clear_cart(
    user_id: str = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    result = await cart_service.clear_cart(user_id)
    return success_response(data=result, message="Cart cleared")
