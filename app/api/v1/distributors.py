from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse
from app.core.redis import get_cache, set_cache

router = APIRouter()

@router.get("/products", response_model=List[ProductResponse])
def search_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    cache_key = f"products:{category}:{min_price}:{max_price}:{search}"
    cached_data = get_cache(cache_key)

    if cached_data:
        print("⚡ CACHE HIT (Fetched from RAM)")
        return cached_data
    print("🐢 CACHE MISS (Fetching from DB)")
    query = db.query(Product)

    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
        
    if min_price:
        query = query.filter(Product.price >= min_price)
        
    if max_price:
        query = query.filter(Product.price <= max_price)
        
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    results =  query.all()

    json_compatible_data = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "quantity": p.quantity,
            "farmer_id": p.farmer_id
        } 
        for p in results
    ]
    
    set_cache(cache_key, json_compatible_data, expire=60)
    return results