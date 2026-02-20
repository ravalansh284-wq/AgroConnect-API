from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.analytics import AnalyticsResponse

router = APIRouter()

@router.get("/", response_model=AnalyticsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    total_revenue = db.query(func.sum(Order.total_price)).scalar() or 0.0
    
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    
    total_products = db.query(func.count(Product.id)).scalar() or 0
    
    total_users = db.query(func.count(User.id)).scalar() or 0
    
    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_users": total_users
    }