from fastapi import APIRouter, Depends

from dependencies.auth_dependency import get_current_user, get_user_service
from schemas.users import UserProfileUpdate, UserResponse
from services.user_service import UserService
from shared.schemas.response_schema import UnifiedResponse, success_response

router = APIRouter(tags=["users"])


@router.get("", response_model=UnifiedResponse)
async def get_profile(user=Depends(get_current_user)):
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="Profile fetched successfully",
    )


@router.patch("", response_model=UnifiedResponse)
async def update_profile(
    payload: UserProfileUpdate,
    user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    result = await user_service.update_profile(
        user.id,
        username=payload.username,
        email=payload.email,
    )
    return success_response(
        data=UserResponse.model_validate(result["user"]).model_dump(),
        message="Profile updated successfully",
    )
