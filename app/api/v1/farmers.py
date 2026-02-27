from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from app.api.deps import get_current_user
router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user_role_names = [r.name for r in current_user.roles]
        if "farmer" not in user_role_names:
            raise HTTPException(status_code=403, detail="Only farmers can add products!")

        new_product = Product(
            name=product.name,
            category=product.category,
            price=product.price,
            quantity=product.quantity,
            farmer_id=current_user.id
        )
        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    except Exception as e:
        print(f"🚨 THE REAL ERROR IS: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"REAL ERROR: {str(e)}")