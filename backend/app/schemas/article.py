from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class ArticleRequest(BaseModel) :
    topic: str


class ArticleResponse(BaseModel) :
    id: int
    title: str
    content: str
    url: HttpUrl
    source: str = "wikipedia"
    images: List[HttpUrl] = []
    
    error: Optional[str] = None
    options: List[str] = []
    
    
class PDFResponse(BaseModel) :
    id: int
    title: str
    content: str
    url: str = "Fichier PDF"
    source: str = "PDF"
    images: List[str] = []
    
    error: Optional[str] = None
    options: List[str] = []