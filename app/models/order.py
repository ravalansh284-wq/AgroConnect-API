from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.audit import AuditMixin

class Order(Base, AuditMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String, default="pending")
    product_id = Column(Integer, ForeignKey("products.id"))
    distributor_id = Column(Integer, ForeignKey("users.id"))
    product = relationship("Product")
    
    distributor = relationship("User", back_populates="orders", foreign_keys=[distributor_id])