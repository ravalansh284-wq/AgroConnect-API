from fastapi import FastAPI
from app.core.database import engine
from app.models import models
from app.api.v1 import farmers, distributors, orders

models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="AgroConnect API")

app.include_router(farmers.router, prefix="/api/v1/farmers", tags=["Farmers"])
app.include_router(distributors.router, prefix="/api/v1/distributors", tags=["Distributors"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])

@app.get("/")
def read_root():
    return {"message":"Welcome to AgroConnect API-Day 1 Complete!"}