from fastapi import APIRouter, Depends

from dependencies.auth_dependency import get_auth_service
from schemas.auth import SigninRequest, SignupRequest, TokenRefreshRequest, TokenResponse
from schemas.users import UserResponse
from services.auth_service import AuthService
from shared.schemas.response_schema import UnifiedResponse, success_response

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UnifiedResponse, status_code=201)
async def signup(payload: SignupRequest, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.signup(payload.username, payload.email, payload.password)
    return success_response(
        data={
            "user": UserResponse.model_validate(result["user"]).model_dump(),
            "tokens": TokenResponse(
                access_token=result["access_token"],
                refresh_token=result["refresh_token"],
            ).model_dump(),
        },
        message="Account created successfully",
    )


@router.post("/signin", response_model=UnifiedResponse)
async def signin(payload: SigninRequest, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.signin(payload.username, payload.password)
    return success_response(
        data={
            "user": UserResponse.model_validate(result["user"]).model_dump(),
            "tokens": TokenResponse(
                access_token=result["access_token"],
                refresh_token=result["refresh_token"],
            ).model_dump(),
        },
        message="Sign in successful",
    )


@router.post("/refresh", response_model=UnifiedResponse)
async def refresh(payload: TokenRefreshRequest, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.refresh_token(payload.refresh_token)
    return success_response(
        data=TokenResponse(access_token=result["access_token"]).model_dump(),
        message="Token refreshed",
    )
