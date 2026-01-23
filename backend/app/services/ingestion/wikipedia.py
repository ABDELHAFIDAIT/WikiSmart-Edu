import wikipedia
import requests
from app.core.config import settings


session = requests.Session()
user_agent = f"WikiSmart-Edu/1.0 (contact : {settings.WIKI_CONTACT_EMAIL})"
session.headersx.update({
    "User-Agent" : user_agent
})
wikipedia.requests = session

wikipedia.set_lang("fr")


# Recherche une page Wikipédia et retourne son contenu
def fetch_wiki_page(topic:str) :
    try :
        page = wikipedia.page(topic, auto_suggest=True)
        
        return {
            "title" : page.title ,
            "content" : page.content ,
            "url" : page.url ,
            "images" : page.images ,
            "status" : "success" ,
            "error" : None ,
        }
    
    except wikipedia.exceptions.PageError :
        return {
            "status": "not_found",
            "error": "Page introuvable",
            "options": []
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "options": []
        }