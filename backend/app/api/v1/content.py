from fastapi import APIRouter, HTTPException, Depends, status
from typing import Any

from app.schemas.article import ArticleRequest, ArticleResponse
from app.services.ingestion.wikipedia import fetch_wiki_page
from app.services.ingestion.cleaner import clean_text
from app.api.deps import get_current_user, get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.article import Article


router = APIRouter()

@router.post("/wiki/search", response_model=ArticleResponse)
def search_wikipedia(request: ArticleRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    print(f"Recherche demandée par {current_user.username} : {request.topic}")
    
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
        raise HTTPException(
            status_code=404,
            detail=f"Aucune page Wikipédia trouvée pour '{request.topic}'"
        )
        
    if raw_data["status"] == "error" :
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne : {raw_data['error']}"
        )
    
    cleaned_content = clean_text(raw_data["content"])
    
    new_article = Article(
        title=raw_data["title"],
        url=raw_data["url"],
        content=cleaned_content,
        user_id=current_user.id
    )
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    return ArticleResponse(
        id=new_article.id,
        title=new_article.title,
        content=new_article.content,
        url=new_article.url,
        images=raw_data.get("images", [])
    )