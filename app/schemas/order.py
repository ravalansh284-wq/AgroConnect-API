from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True