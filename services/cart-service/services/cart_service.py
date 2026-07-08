import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.cart_repository import CartRepository
from shared.exceptions import NotFoundError


class CartService:
    def __init__(self, session: AsyncSession):
        self.repo = CartRepository(session)

    async def get_or_create_cart(self, user_id: str | uuid.UUID) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        cart = await self.repo.get_by_user_id(user_id)
        if not cart:
            cart = await self.repo.create(user_id)
        return {"cart": cart}

    async def get_cart(self, user_id: str | uuid.UUID) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        cart = await self.repo.get_by_user_id(user_id)
        if not cart:
            raise NotFoundError("Cart not found")
        return {"cart": cart}

    async def add_item(
        self, user_id: str | uuid.UUID, product_id: uuid.UUID, quantity: int, price: float
    ) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        cart = await self.repo.get_by_user_id(user_id)
        if not cart:
            cart = await self.repo.create(user_id)
        item = await self.repo.add_item(cart.id, product_id, quantity, price)
        return {"item": item}

    async def update_item(
        self, user_id: str | uuid.UUID, item_id: uuid.UUID, quantity: int
    ) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        cart = await self.repo.get_by_user_id(user_id)
        if not cart:
            raise NotFoundError("Cart not found")
        item = await self.repo.get_item(item_id)
        if not item or item.cart_id != cart.id:
            raise NotFoundError("Cart item not found")
        updated = await self.repo.update_item(item, quantity=quantity)
        return {"item": updated}

    async def remove_item(self, user_id: str | uuid.UUID, item_id: uuid.UUID) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        cart = await self.repo.get_by_user_id(user_id)
        if not cart:
            raise NotFoundError("Cart not found")
        item = await self.repo.get_item(item_id)
        if not item or item.cart_id != cart.id:
            raise NotFoundError("Cart item not found")
        await self.repo.delete_item(item)
        return {"message": "Item removed from cart"}

    async def clear_cart(self, user_id: str | uuid.UUID) -> dict:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        cart = await self.repo.get_by_user_id(user_id)
        if not cart:
            raise NotFoundError("Cart not found")
        await self.repo.clear_items(cart.id)
        return {"message": "Cart cleared"}
