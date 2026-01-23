import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.core.config import settings
import io




def get_auth_headers(client: TestClient):
    """Crée un user et retourne le header d'auth."""
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "tester@test.com", "username": "tester", "password": "password123"}
    )
    login = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "tester", "password": "password123"}
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}





def test_search_wikipedia_success(client: TestClient):
    """
    Teste le flux complet : Recherche Wiki -> Sauvegarde en BDD -> Retour JSON.
    """
    headers = get_auth_headers(client)
    
    # On mock 'fetch_wiki_page' là où il est utilisé dans l'API (api/v1/content.py)
    with patch("app.api.v1.content.fetch_wiki_page") as mock_fetch:
        # 1. Configurer le Mock pour simuler une réponse positive de Wikipédia
        mock_fetch.return_value = {
            "status": "success",
            "title": "Intelligence Artificielle",
            "content": "L'IA est un domaine de l'informatique...",
            "url": "https://fr.wikipedia.org/wiki/IA",
            "images": [],
            "error": None
        }

        # 2. Appel API
        response = client.post(
            f"{settings.API_V1_STR}/wiki/search",
            headers=headers,
            json={"topic": "IA"} # 'topic' est le champ important
        )

        # 3. Vérifications
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Intelligence Artificielle"
        assert data["id"] is not None # L'article a bien été créé en BDD




def test_search_wikipedia_not_found(client: TestClient):
    """
    Teste le cas où Wikipédia ne trouve rien.
    """
    headers = get_auth_headers(client)

    with patch("app.api.v1.content.fetch_wiki_page") as mock_fetch:
        mock_fetch.return_value = {
            "status": "not_found",
            "error": "Page introuvable",
            "options": []
        }

        response = client.post(
            f"{settings.API_V1_STR}/wiki/search",
            headers=headers,
            json={"topic": "SujetInexistant12345"}
        )
        
        # Selon votre implémentation, ça peut être 404
        assert response.status_code == 404
        assert "Aucune page Wikipédia trouvée" in response.json()["detail"]




def test_upload_pdf_success(client: TestClient):
    """
    Teste l'upload d'un fichier PDF simulé.
    """
    headers = get_auth_headers(client)

    # 1. Créer un faux fichier PDF en mémoire
    fake_pdf = io.BytesIO(b"%PDF-1.4 ... content ...")
    fake_pdf.name = "cours_test.pdf"

    # 2. Mocker l'extracteur LangChain pour ne pas parser le binaire pour de vrai
    with patch("app.api.v1.content.extract_text_from_pdf") as mock_extract:
        mock_extract.return_value = "Contenu extrait du PDF de test."

        # 3. Envoyer le fichier (multipart/form-data)
        # Note: requests/TestClient gère le Content-Type automatiquement avec 'files'
        response = client.post(
            f"{settings.API_V1_STR}/upload/pdf",
            headers=headers,
            files={"file": ("cours_test.pdf", fake_pdf, "application/pdf")}
        )

        assert response.status_code == 200
        data = response.json()
        assert "[PDF]" in data["title"]
        assert data["content"] == "Contenu extrait du PDF de test."