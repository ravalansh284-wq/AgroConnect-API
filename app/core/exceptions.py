from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

async def database_exception_handler(request: Request,exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "success":False,
            "error_code":"DATABSE_ERROR",
            "message":"A database error occurred",
            "detail":str(exc.__dict__.get("orig",str(exc)))
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error_code": "VALIDATION_ERROR",
            "message": "Invalid data provided.",
            "detail": exc.errors()
        }
    )

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Something went wrong.",
            "detail": str(exc)
        }
    )