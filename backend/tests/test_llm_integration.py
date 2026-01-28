import pytest
from fastapi.testclient import TestClient
from app.core.config import settings
from unittest.mock import patch


def get_auth_token(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "user@gmail.com", "username": "user", "password": "password123"}
    )

    res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "user", "password": "password123"}
    )
    
    assert res.status_code == 200, f"Login failed: {res.text}"
    return res.json()["access_token"]



def create_test_article(client: TestClient, headers: dict):
    with patch("app.api.v1.content.fetch_wiki_page") as mock_wiki:
        mock_wiki.return_value = {
            "status": "success",
            "title": "Article Test Integration",
            "content": "Contenu de test pour validation des services IA.",
            "url": "http://fake.url/wiki_test",
            "images": [],
            "error": None
        }
        res = client.post(
            f"{settings.API_V1_STR}/wiki/search",
            headers=headers,
            json={"topic": "Integration Test"}
        )
        assert res.status_code == 200
        return res.json()





def test_summary_generation(client: TestClient, mock_groq):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    article = create_test_article(client, headers)
    
    response = client.post(
        f"{settings.API_V1_STR}/ai/summary",
        headers=headers,
        json={"article_id": article["id"]}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Résumé" in data["result"]
    
    mock_groq.assert_called_once()




def test_translation_generation(client: TestClient, mock_gemini):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    article = create_test_article(client, headers)
    
    response = client.post(
        f"{settings.API_V1_STR}/ai/translate",
        headers=headers,
        json={"article_id": article["id"], "target_lang": "anglais"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Traduction" in data["result"]
    
    mock_gemini.translate_article.assert_called_once()




def test_quiz_generation(client: TestClient, mock_gemini):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    article = create_test_article(client, headers)
    
    response = client.post(
        f"{settings.API_V1_STR}/ai/quiz/generate",
        headers=headers,
        json={"article_id": article["id"]}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["article_id"] == article["id"]
    assert len(data["questions"]) >= 1
    assert "options" in data["questions"][0]
    
    mock_gemini.generate_quiz.assert_called_once()