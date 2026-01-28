import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.core.config import settings
import io




def get_auth_headers(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "user@gmail.com", "username": "user", "password": "password123"}
    )
    login = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "user", "password": "password123"}
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}





def test_search_wikipedia_success(client: TestClient):
    headers = get_auth_headers(client)
    
    with patch("app.api.v1.content.fetch_wiki_page") as mock_fetch:
        mock_fetch.return_value = {
            "status": "success",
            "title": "Intelligence Artificielle",
            "content": "L'IA est un domaine de l'informatique...",
            "url": "https://fr.wikipedia.org/wiki/IA",
            "images": [],
            "error": None
        }

        response = client.post(
            f"{settings.API_V1_STR}/wiki/search",
            headers=headers,
            json={"topic": "IA"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Intelligence Artificielle"
        assert data["id"] is not None





def test_search_wikipedia_not_found(client: TestClient):
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
        
        assert response.status_code == 404
        assert "Aucune page Wikipédia trouvée" in response.json()["detail"]





def test_upload_pdf_success(client: TestClient):
    headers = get_auth_headers(client)

    fake_pdf = io.BytesIO(b"%PDF-1.4 ... content ...")
    fake_pdf.name = "cours_test.pdf"

    with patch("app.api.v1.content.extract_text_from_pdf") as mock_extract:
        mock_extract.return_value = "Contenu extrait du PDF de test."

        response = client.post(
            f"{settings.API_V1_STR}/upload/pdf",
            headers=headers,
            files={"file": ("cours_test.pdf", fake_pdf, "application/pdf")}
        )

        assert response.status_code == 200
        data = response.json()
        assert "[PDF]" in data["title"]
        assert data["content"] == "Contenu extrait du PDF de test."