from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.audit import AuditMixin
class Product(Base,AuditMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    farmer_id = Column(Integer, ForeignKey("users.id"))

    farmer = relationship("User", back_populates="products", foreign_keys=[farmer_id])