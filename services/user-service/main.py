from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from api.v1.auth import router as auth_router
from api.v1.users import router as users_router
from core.config import settings
from db.session import init_db
from shared.exceptions import AppException, app_exception_handler, universal_error_response
from shared.schemas.response_schema import error_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, lambda req, exc: error_response(str(exc), 422))
app.add_exception_handler(HTTPException, lambda req, exc: error_response(exc.detail, exc.status_code))
app.add_exception_handler(Exception, universal_error_response)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/me", tags=["users"])


@app.get("/health")
async def health():
    return {"status": "ok"}
