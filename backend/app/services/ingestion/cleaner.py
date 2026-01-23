import re



def clean_whitespace(text: str) -> str:
    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text)
    return text.strip()



def clean_wiki_text(text: str) :
    if not text :
        return ""
    
    text = re.sub(r'\[.*?\]', '', text)
    
    markers = [
        "== Voir aussi ==",
        "== Notes et références ==", 
        "== Bibliographie ==", 
        "== Liens externes =="
    ]
    
    for marker in markers :
        if marker in text :
            text = text.split(marker)[0]
            
    return clean_whitespace(text)



def split_text(text: str, max_chars: int = 3000) :
    if len(text) <= max_chars :
        return [text]
    
    chunks = []
    
    for i in range(0, len(text), max_chars) :
        chunks.append(text[i: i + max_chars])
        
    return chunks




def clean_pdf_text(text: str) -> str:
    if not text:
        return ""
    
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    
    return clean_whitespace(text)