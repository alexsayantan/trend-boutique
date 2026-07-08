import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.session import get_session
from repositories.cart_repository import CartRepository
from services.cart_service import CartService
from shared.exceptions import UnauthorizedError
from shared.utils.auth_utils import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


async def get_cart_service(session: AsyncSession = Depends(get_session)) -> CartService:
    return CartService(session)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    payload = verify_token(token)
    if not payload:
        raise UnauthorizedError("Invalid or expired token")
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")
    return user_id


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = CartRepository(session)
    user = await repo.get_by_user_id(uuid.UUID(user_id))
    if not user:
        raise UnauthorizedError("User not found")
    return user
