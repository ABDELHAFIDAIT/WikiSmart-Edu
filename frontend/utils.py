import requests

API_URL = "http://127.0.0.1:8000/api/v1"



def login_request(username, password):
    url = f"{API_URL}/auth/login"
    payload = {"username": username, "password": password}
    
    try:
        response = requests.post(url, data=payload)
        return response
    except:
        return None




def signup_request(email, username, password):
    url = f"{API_URL}/auth/signup"
    payload = {"email": email, "username": username, "password": password}
    
    try:
        response = requests.post(url, json=payload)
        return response
    except:
        return None




def get_user_profile(token):
    url = f"{API_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        return response
    except:
        return None