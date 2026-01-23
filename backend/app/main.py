from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, content, ai_tools, users
from contextlib import asynccontextmanager
from app.core.init_db import init_db
from app.core.database import SessionLocal
from app.core.logging import setup_logging
from app.core.exceptions import global_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    yield
    pass

app = FastAPI(
    title="WikiSmart Edu API",
    description="API pour l'application éducative WikiSmart (Traduction, génération de quiz et résumés via IA)",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Durée: {process_time:.2f}s"
    )
    
    return response


app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(content.router, prefix=settings.API_V1_STR, tags=["Wikipedia"])
app.include_router(ai_tools.router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI Tools"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])

@app.get("/")
def root() :
    return {
        "message": "Bienvenue sur l'API WikiSmart Edu !",
        "status": "online",
        "docs_url": "/docs"
    }