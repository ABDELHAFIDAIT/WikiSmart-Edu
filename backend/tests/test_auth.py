from fastapi.testclient import TestClient
from app.core.config import settings

def test_signup_new_user(client: TestClient):
    """
    Teste l'inscription d'un nouvel utilisateur.
    Doit renvoyer 200 OK et les infos de l'utilisateur (sans le mot de passe).
    """
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Sécurité




def test_signup_existing_email(client: TestClient):
    """
    Teste qu'on ne peut pas créer deux comptes avec le même email.
    """
    # 1. Premier compte
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "duplicate@example.com", "username": "u1", "password": "pwd"}
    )
    
    # 2. Tentative de doublon
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "duplicate@example.com", "username": "u2", "password": "pwd"}
    )
    assert response.status_code == 400
    assert "Cet email est déjà utilisé !" in response.text





def test_login_success(client: TestClient):
    """
    Teste la connexion et la récupération du Token JWT.
    """
    # 1. Inscription
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "login@example.com", "username": "loginuser", "password": "password123"}
    )
    
    # 2. Login (Format OAuth2 form-data)
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"





def test_login_wrong_password(client: TestClient):
    """
    Teste le rejet d'un mauvais mot de passe.
    """
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "wrongpwd@example.com", "username": "wrong", "password": "correctpassword"}
    )
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "wrong", "password": "wrongpassword"}
    )
    assert response.status_code == 401





def test_read_users_me_no_token(client: TestClient):
    """
    Vérifie qu'une route protégée rejette un accès sans token.
    """
    response = client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == 401





def test_read_users_me_with_token(client: TestClient):
    """
    Vérifie qu'une route protégée accepte un accès avec un token valide.
    """
    # 1. Inscription
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "me@example.com", "username": "me", "password": "pwd"}
    )
    
    # 2. Login pour avoir le token
    login_res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "me", "password": "pwd"}
    )
    token = login_res.json()["access_token"]
    
    # 3. Accès protégé
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"