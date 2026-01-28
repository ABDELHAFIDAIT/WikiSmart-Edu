from fastapi.testclient import TestClient
from app.core.config import settings

def test_signup_new_user(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "user@gmail.com",
            "username": "user",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@gmail.com"
    assert "id" in data
    assert "hashed_password" not in data




def test_signup_existing_email(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "user@gmail.com", "username": "user", "password": "password123"}
    )
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "user@gmail.com", "username": "user", "password": "password123"}
    )
    assert response.status_code == 400
    assert "Cet email est déjà utilisé !" in response.text





def test_login_success(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "user@gmail.com", "username": "user", "password": "password123"}
    )
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "user", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"





def test_login_wrong_password(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "user@gmail.com", "username": "user", "password": "password123"}
    )
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "user", "password": "password321"}
    )
    assert response.status_code == 401





def test_read_users_me_no_token(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == 401





def test_read_users_me_with_token(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "user@gmail.com", "username": "user", "password": "password123"}
    )
    
    login_res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "user", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["email"] == "user@gmail.com"