from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import  Session
from app.core.database import get_db
from app.models.models import Order, Product, User
from app.schemas.order import OrderCreate, OrderResponse
from app.services.email import send_order_confirmation

router = APIRouter()

@router.post("order",response_model=OrderResponse)
def create_order(order: OrderCreate,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == order.product_id).with_for_update().first()

    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    
    if product.quantity < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    total_cost = product.price * order.quantity

    new_order = Order(
        product_id=order.product_id,
        distributor_id=1,
        quantity=order.quantity,
        total_price=total_cost,
        status="completed"
    ) 

    try:
        product.quantity -= order.quantity
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        background_tasks.add_task(send_order_confirmation, "distributor@example.com", new_order.id)

        return new_order
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))