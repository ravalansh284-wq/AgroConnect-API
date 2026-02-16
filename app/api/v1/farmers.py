from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from app.api.deps import get_current_user
router = APIRouter()

@router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # <--- 🔒 THIS LOCKS THE DOOR
):
    # 1. Enforce Role: Only Farmers
    if current_user.role != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can add products!")

    # 2. Create Product (Linked to the REAL User)
    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        quantity=product.quantity,
        farmer_id=current_user.id  # <--- Using the token's user ID
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product