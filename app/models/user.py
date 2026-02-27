from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.audit import AuditMixin
from app.models.role import user_roles

class User(Base, AuditMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    roles = relationship("Role", secondary=user_roles, backref="users")
    products = relationship("Product", back_populates="farmer",foreign_keys="Product.farmer_id")
    orders = relationship("Order",back_populates="distributor",foreign_keys="Order.distributor_id")