import asyncio
from fastapi import FastAPI
from api.v1.categories import router as category_router
from api.v1.products import router as product_router
from db.session import engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Product Service",
    description="Catalog management for Trend Boutique",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    # In a real app we'd use Alembic, but for this scaffolding:
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

app.include_router(category_router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(product_router, prefix="/api/v1/products", tags=["Products"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
