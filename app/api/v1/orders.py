from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from typing import List

router = APIRouter()
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    order_data: OrderCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_role_names = [r.name for r in current_user.roles]
    if "distributor" not in user_role_names:
        raise HTTPException(status_code=403, detail="Only distributors can buy products!")
    
    product = db.query(Product).filter(Product.id == order_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
 
    if product.quantity < order_data.quantity:
        raise HTTPException(status_code=400, detail=f"Not enough stock! Only {product.quantity} available.")

    total_bill = product.price * order_data.quantity

    new_order = Order(
        quantity=order_data.quantity,
        total_price=total_bill,
        status="pending",
        distributor_id=current_user.id,
        product_id=product.id
    )

    product.quantity -= order_data.quantity

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return OrderResponse(
        id=new_order.id,
        product_name=product.name,
        quantity=new_order.quantity,
        total_price=new_order.total_price,
        status=new_order.status
    )

@router.get("/", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user_role_names = [r.name for r in current_user.roles]
        
        if "distributor" in user_role_names:
            orders = db.query(Order).filter(Order.distributor_id == current_user.id).all()
        else:
            orders = (
                db.query(Order)
                .join(Product)
                .filter(Product.farmer_id == current_user.id)
                .all()
            )
        
        results = []
        for o in orders:
            # We use a dictionary here to prevent Pydantic serialization crashes
            results.append({
                "id": o.id,
                "product_name": o.product.name if o.product else "Unknown Product", 
                "quantity": o.quantity,
                "total_price": o.total_price,
                "status": o.status
            })
        
        return results

    except Exception as e:
        print(f"🚨 THE REAL ERROR IS: {e}")
        raise HTTPException(status_code=500, detail=f"REAL ERROR: {str(e)}")