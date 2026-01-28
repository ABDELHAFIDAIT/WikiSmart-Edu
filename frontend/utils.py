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
    
    

def search_wiki(token, topic):
    url = f"{API_URL}/wiki/search"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"topic": topic}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response
    except:
        return None
    


def generate_summary_request(token, article_id):
    url = f"{API_URL}/ai/summary"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"article_id": article_id}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response
    except:
        return None