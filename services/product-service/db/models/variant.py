import uuid
from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from db.session import Base

class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    attributes = Column(JSONB, nullable=False, default={}) # e.g., {"color": "red", "size": "M"}
    price_override = Column(Numeric(10, 2), nullable=True) # Optional price specific to this variant

    product = relationship("Product", back_populates="variants")
