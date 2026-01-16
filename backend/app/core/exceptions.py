from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logging import logger

async def global_exception_handler(request: Request, exc: Exception):
    
    logger.error(f"ERREUR CRITIQUE sur {request.url} : {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Une erreur interne est survenue !"}
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"Erreur HTTP {exc.status_code} sur {request.url} : {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )