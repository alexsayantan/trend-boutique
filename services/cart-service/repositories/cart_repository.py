import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models.cart import Cart, CartItem


class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: uuid.UUID) -> Cart | None:
        result = await self.session.execute(
            select(Cart)
            .options(selectinload(Cart.items))
            .where(Cart.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID) -> Cart:
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        await self.session.commit()
        await self.session.refresh(cart)
        return cart

    async def add_item(
        self, cart_id: uuid.UUID, product_id: uuid.UUID, quantity: int, price: float
    ) -> CartItem:
        item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity, price=price)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_item(self, item_id: uuid.UUID) -> CartItem | None:
        result = await self.session.execute(select(CartItem).where(CartItem.id == item_id))
        return result.scalar_one_or_none()

    async def update_item(self, item: CartItem, **kwargs) -> CartItem:
        for key, value in kwargs.items():
            if value is not None:
                setattr(item, key, value)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_item(self, item: CartItem) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def clear_items(self, cart_id: uuid.UUID) -> None:
        await self.session.execute(
            select(CartItem).where(CartItem.cart_id == cart_id)
        )
        await self.session.execute(
            CartItem.__table__.delete().where(CartItem.cart_id == cart_id)
        )
        await self.session.commit()
