from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, data: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.data = data


class BadRequestError(AppException):
    def __init__(self, message: str = "Bad request", data: dict | None = None):
        super().__init__(message=message, status_code=400, data=data)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized", data: dict | None = None):
        super().__init__(message=message, status_code=401, data=data)


class NotFoundError(AppException):
    def __init__(self, message: str = "Not found", data: dict | None = None):
        super().__init__(message=message, status_code=404, data=data)


class ConflictError(AppException):
    def __init__(self, message: str = "Conflict", data: dict | None = None):
        super().__init__(message=message, status_code=409, data=data)


def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message, "data": exc.data},
    )


def universal_error_response(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"},
    )
