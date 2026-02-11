from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Product, User
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        quantity=product.quantity,
        farmer_id=1  
    )

    db.add(new_product)
    db.commit()    
    db.refresh(new_product)
    
    return new_product