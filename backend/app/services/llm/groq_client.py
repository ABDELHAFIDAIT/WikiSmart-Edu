from groq import Groq
from app.core.config import settings


class GroqService() :
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        
    def generate_summary(self, text: str) :
        if not text :
            return "Aucun texte à résumer !"
        
        text_chunk = text[:15000]
        
        system_prompt = (
            "Tu es un assistant pédagogique expert. "
            "Ton objectif est de synthétiser des articles complexes pour des étudiants. "
            "Règles : "
            "1. Fais un résumé clair et structuré en Français. "
            "2. Utilise des listes à puces (bullet points) pour les idées clés. "
            "3. Sois concis (maximum 300 mots). "
            "4. Utilise un ton neutre et éducatif."
        )
        
        # system_prompt = (
        #     "Tu es un assistant pédagogique expert, spécialisé dans la vulgarisation de contenus académiques et techniques. "
        #     "Ta mission est de transformer des articles complexes en résumés clairs et accessibles pour des étudiants. "
        #     "Consignes : "
        #     "1. Rédige un résumé structuré et cohérent en français. "
        #     "2. Commence par une phrase d’introduction qui présente le sujet général. "
        #     "3. Présente les idées essentielles sous forme de listes à puces claires et hiérarchisées. "
        #     "4. Reformule avec tes propres mots, sans copier le texte original. "
        #     "5. Élimine les détails secondaires et conserve uniquement l’information à forte valeur pédagogique. "
        #     "6. Utilise un vocabulaire simple et précis, en évitant le jargon inutile. "
        #     "7. Respecte une longueur maximale de 300 mots. "
        #     "8. Adopte un ton neutre, clair et éducatif."
        # )

        try :
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role":"system", "content": system_prompt},
                    {"role":"user", "content": f"Résumer ce texte : \n\n{text_chunk}"},
                ],
                model=self.model,
                temperature=0.3
            )
            
            return chat_completion.choices[0].message.content
        
        except Exception as e :
            print(f"Erreur Groq : {e}")
            return "Erreur lors de la génération du résumé avec Groq !"


groq_service = GroqService()