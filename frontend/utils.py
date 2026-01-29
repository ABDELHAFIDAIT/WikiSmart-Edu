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




def translate_article_request(token, article_id, target_lang):
    url = f"{API_URL}/ai/translate"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"article_id": article_id, "target_lang": target_lang}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response
    except:
        return None
    
    
    
def generate_quiz_request(token, article_id):
    url = f"{API_URL}/ai/quiz/generate"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"article_id": article_id}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response
    except:
        return None




def submit_quiz_request(token, quiz_id, answers):
    url = f"{API_URL}/ai/quiz/submit"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"quiz_id": quiz_id, "user_answers": answers}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response
    except:
        return None
    
    
def get_history_articles(token):
    url = f"{API_URL}/users/me/history/articles"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        return requests.get(url, headers=headers)
    except:
        return None




def get_full_article(token, article_id):
    url = f"{API_URL}/users/me/history/articles/{article_id}/full"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        return requests.get(url, headers=headers)
    except:
        return None



def upload_pdf_request(token, file_obj):
    url = f"{API_URL}/upload/pdf"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (file_obj.name, file_obj, "application/pdf")}
    
    try:
        response = requests.post(url, files=files, headers=headers)
        return response
    except:
        return None
    

def update_password_request(token, old_pass, new_pass):
    url = f"{API_URL}/users/me/password"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"old_password": old_pass, "new_password": new_pass}
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        return response
    except:
        return None