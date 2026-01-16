import google.generativeai as genai
from app.core.config import settings
import json


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
    
    
    
    def generate_quiz(self, text: str, num_questions: int = 5) :
        if not text :
            return []
        
        prompt = (
            f"Tu es un générateur de quiz API. "
            f"Génère {num_questions} questions QCM basées sur le texte ci-dessous."
            "RÈGLES STRICTES DE SORTIE :"
            "1. Renvoie UNIQUEMENT un tableau JSON (Array of Objects)."
            "2. Chaque objet DOIT avoir EXACTEMENT ces clés : 'id', 'question', 'options', 'correct_index'."
            "3. 'options' est une liste de 4 chaines de caractères."
            "4. 'correct_index' est un entier (0, 1, 2 ou 3)."
            f"\n\nTexte source :\n{text[:20000]}"
        )
        
        try :
            response = self.model.generate_content(prompt)
            raw_text = response.text
            
            cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()
            
            quiz_data = json.loads(cleaned_text)
            # return quiz_data

            validated_quiz = []
            for i, item in enumerate(quiz_data):
                question_text = item.get("question") or item.get("text") or item.get("query")
                options = item.get("options") or item.get("choices") 
                correct_idx = item.get("correct_index")
                
            
                if correct_idx is None and "answer" in item:
                    correct_idx = item["answer"]

            
                if question_text and options and isinstance(options, list) and correct_idx is not None:
                    validated_quiz.append({
                        "id": i + 1,
                        "question": question_text,
                        "options": options[:4],
                        "correct_index": int(correct_idx)
                    })
            
            return validated_quiz            
        except json.JSONDecodeError:
            print("Erreur : L'IA n'a pas renvoyé du JSON valide.")
            return []
        
        except Exception as e:
            print(f"Erreur Gemini Quiz : {e}")
            return []
        
        
gemini_service = GeminiService()