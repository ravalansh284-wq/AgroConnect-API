from fastapi import FastAPI
from app.core.database import engine,Base
from app.models import user,product,order
from app.api.v1 import farmers, distributors, orders
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import(database_exception_handler,validation_exception_handler,global_exception_handler)
from app.api.v1 import auth
from app.api.v1 import farmers, distributors, orders, auth, analytics
from app.core.middleware import AuditMiddleware
from app.core.audit_listener import register_audit_listeners
Base.metadata.create_all(bind=engine)
register_audit_listeners()
app=FastAPI(title="AgroConnect API")

app.add_exception_handler(SQLAlchemyError,database_exception_handler)
app.add_exception_handler(RequestValidationError,validation_exception_handler)
app.add_exception_handler(Exception,global_exception_handler)
app.include_router(farmers.router, prefix="/api/v1/farmers", tags=["Farmers"])
app.include_router(distributors.router, prefix="/api/v1/distributors", tags=["Distributors"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(auth.router,prefix="/api/v1/auth",tags=["Authentication"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics 📊"]) 
app.add_middleware(AuditMiddleware)
@app.get("/")
def read_root():
    return {"message":"Welcome to AgroConnect API-Day 1 Complete!"}