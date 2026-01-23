from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from typing import Any

from app.schemas.article import ArticleRequest, ArticleResponse, PDFResponse
from app.services.ingestion.wikipedia import fetch_wiki_page
from app.services.ingestion.cleaner import clean_wiki_text
from app.api.deps import get_current_user, get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.article import Article
from app.core.logging import logger

import shutil
from app.services.ingestion.pdf_loader import extract_text_from_pdf
import os



router = APIRouter()

@router.post("/wiki/search", response_model=ArticleResponse)
def search_wikipedia(request: ArticleRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    logger.info(f"Recherche Wikipedia : '{request.topic}' par User ID {current_user.id}")
    
    raw_data = fetch_wiki_page(request.topic)
    
    if raw_data["status"] == "ambiguous" :
        return ArticleResponse(
            id=0,
            title="Sujet ambigu",
            content="",
            url="https://fr.wikipedia.org",
            error=raw_data["error"],
            options=raw_data["options"]
        )
    
    if raw_data["status"] == "not_found" :
        logger.warning(f"Aucune page trouvée pour : {request.topic}")
        raise HTTPException(
            status_code=404,
            detail=f"Aucune page Wikipédia trouvée pour '{request.topic}'"
        )
        
    if raw_data["status"] == "error" :
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne : {raw_data['error']}"
        )
        
    cleaned_content = clean_wiki_text(raw_data["content"])
    
    new_article = Article(
        title=raw_data["title"],
        url=raw_data["url"],
        content=cleaned_content,
        user_id=current_user.id
    )
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    logger.info(f"Article trouvé et sauvegardé : {raw_data['title']}")
    
    return ArticleResponse(
        id=new_article.id,
        title=new_article.title,
        content=new_article.content,
        url=new_article.url,
        images=raw_data.get("images", [])
    )
    
    

@router.post("/upload/pdf", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    logger.info(f"Réception du fichier PDF : {file.filename} par User {current_user.id}")
    
    temp_filename = f"temp_{file.filename}"
    try :
        with open(temp_filename, "wb") as buffer :
            shutil.copyfileobj(file.file, buffer)
            
        extracted_text = extract_text_from_pdf(temp_filename)
        
        if not extracted_text :
            raise HTTPException(status_code=400, detail="Impossible d'extraire du texte du PDF !")
        
        new_article = Article(
            title = f"[PDF] {file.filename}",
            content = extracted_text,
            url = "Fichier PDF",
            user_id = current_user.id
        )
        
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        logger.info(f"PDF traité avec Succès : {new_article.title}")
        
        return PDFResponse(
            id=new_article.id,
            title=new_article.title,
            content=new_article.content,
            url=new_article.url,
            images=[]
        )
        
    except Exception as e :
        logger.error(f"Erreur upload PDF : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur Traitement PDF : {str(e)}")
    
    finally :
        if os.path.exists(temp_filename):
            os.remove(temp_filename)