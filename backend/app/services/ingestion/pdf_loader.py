from langchain_community.document_loaders import PyPDFLoader
from app.services.ingestion.cleaner import clean_pdf_text
import os


def extract_text_from_pdf(file_path: str) :
    try :
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        full_text = "\n\n".join([page.page_content for page in pages])
        
        cleaned_content = clean_pdf_text(full_text)
        
        return cleaned_content
    
    except Exception as e :
        print(f"Erreur lors de la lecture du PDF : {e}")
        return ""