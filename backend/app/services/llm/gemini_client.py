import google.generativeai as genai
from app.core.config import settings


class GeminiService() :
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    
    def translate_article(self, text:str, target_lang: str) :
        if not text :
            return "Aucun texte à traduire."
        
        prompt = (
            f"Tu es un traducteur professionnel. "
            f"Traduis le texte suivant en **{target_lang}**. "
            "Règles :"
            "1. Garde le ton éducatif et précis."
            "2. Ne traduis pas les noms propres techniques s'ils sont universels."
            "3. Renvoie UNIQUEMENT la traduction, pas de blabla avant ou après."
            f"\n\nTexte à traduire :\n{text[:25000]}"
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erreur Gemini : {e}")
            return f"Erreur lors de la traduction : {str(e)}"
        
gemini_service = GeminiService()