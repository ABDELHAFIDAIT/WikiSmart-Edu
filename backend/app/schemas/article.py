from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class ArticleRequest(BaseModel) :
    topic: str


class ArticleResponse(BaseModel) :
    title: str
    content: str
    url: HttpUrl
    source: str = "wikipedia"
    images: List[HttpUrl] = []
    
    error: Optional[str] = None
    options: List[str] = []