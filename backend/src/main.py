from uuid import uuid4
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.boostrap import app
from src.logger import logger
from fastapi.exception_handlers import http_exception_handler

@app.exception_handler(ValidationError)
async def unicorn_exception_handler(request: Request, exc: ValidationError):
    errors = [{"field": a["loc"][0], "message": a["msg"]} for a in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={"errors": errors},
    )


@app.exception_handler(Exception)
async def json_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    error_code = uuid4()
    logger.error(f"Error code: {error_code}")
    body = await request.body()
    logger.error(f"Request Body: {str(body)}")
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error. Error code: {error_code}"},
    )
