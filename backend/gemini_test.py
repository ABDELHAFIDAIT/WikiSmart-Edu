import google.generativeai as genai
import os
from dotenv import load_dotenv

# Charge la clé depuis le .env
load_dotenv(dotenv_path="backend/.env") 
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Erreur : Clé GEMINI_API_KEY introuvable dans le .env")
else:
    genai.configure(api_key=api_key)
    print(f"✅ Clé trouvée : {api_key[:5]}...")
    
    print("\n🔍 Recherche des modèles disponibles...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")