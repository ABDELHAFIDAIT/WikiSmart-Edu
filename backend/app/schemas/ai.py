from pydantic import BaseModel

class AIRequest(BaseModel) :
    article_id: int


class TranslationRequest(BaseModel) :
    article_id: int
    target_lang: str = "Anglais"


class ActionResponse(BaseModel) :
    id: int
    article_id: int
    action_type: str
    result: str
    created_at: str