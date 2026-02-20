from pydantic import BaseModel

class AnalyticsResponse(BaseModel):
    total_revenue: float
    total_orders: int
    total_products: int
    total_users: int