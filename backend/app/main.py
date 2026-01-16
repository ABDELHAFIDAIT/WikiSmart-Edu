from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, content, ai_tools
from contextlib import asynccontextmanager
from app.core.init_db import init_db
from app.core.database import SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
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

@app.get("/")
def root() :
    return {
        "message": "Bienvenue sur l'API WikiSmart Edu !",
        "status": "online",
        "docs_url": "/docs"
    }