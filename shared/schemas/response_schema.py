from typing import Generic, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class UnifiedResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: T | None = None


def success_response(data: T | None = None, message: str = "Success") -> UnifiedResponse[T]:
    return UnifiedResponse(success=True, message=message, data=data)


def error_response(message: str = "Error", status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=UnifiedResponse(success=False, message=message).model_dump(),
    )
