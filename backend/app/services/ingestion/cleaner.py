import re


def clean_text(text: str) :
    if not text :
        return ""
    
    # Supprimer les références entre crochets (ex: [12], [citation nécessaire])
    text = re.sub(r'\[.*?\]', '', text)
    
    # Supprimer les espaces multiples (ex: "Bonjour    monde" -> "Bonjour monde")
    text = re.sub(r'\s+', ' ', text)
    
    markers = [
        "== Voir aussi ==",
        "== Notes et références ==", 
        "== Bibliographie ==", 
        "== Liens externes =="
    ]
    
    for marker in markers :
        if marker in text :
            text = text.split(marker)[0]
            
    return text.strip()



def split_text(text: str, max_chars: int = 3000) :
    if len(text) <= max_chars :
        return [text]
    
    chunks = []
    
    for i in range(0, len(text), max_chars) :
        chunks.append(text[i: i + max_chars])
        
    return chunks
