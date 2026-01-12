from fastapi import APIRouter, HTTPException, Depends, status
from typing import Any

from app.schemas.article import ArticleRequest, ArticleResponse
from app.services.ingestion.wikipedia import fetch_wiki_page
from app.services.ingestion.cleaner import clean_text
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter()

@router.post("/wiki/search", response_model=ArticleRequest)
def search_wikipedia(request: ArticleRequest, current_user: User = Depends(get_current_user)) :
    print(f"Recherche demandée par {current_user.username} : {request.topic}")
    
    raw_data = fetch_wiki_page(request.topic)
    
    if raw_data["status"] == "ambiguous" :
        return ArticleResponse(
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
    
    return ArticleResponse(
        title=raw_data["title"],
        content=cleaned_content,
        url=raw_data["url"],
        images=raw_data.get("images", [])
    )