import streamlit as st
from utils import login_request, signup_request, get_user_profile


st.set_page_config(page_title="WikiSmart Edu")


if 'token' not in st.session_state:
    st.session_state['token'] = None

st.title("WikiSmart Edu")

if st.session_state['token'] is None:
    
    choix = st.sidebar.selectbox("Menu", ["Connexion", "Inscription"])
    
    if choix == "Connexion":
        st.subheader("Se connecter")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        bouton_login = st.button("Valider")
        
        if bouton_login:
            reponse = login_request(username, password)
            
            if reponse and reponse.status_code == 200:
                data = reponse.json()
                st.session_state['token'] = data['access_token']
                st.success("Connexion reussie")
                st.rerun()
            else:
                st.error("Erreur de connexion. Verifiez vos identifiants.")

    elif choix == "Inscription":
        st.subheader("Creer un compte")
        email = st.text_input("Email")
        new_user = st.text_input("Nom d'utilisateur")
        new_pass = st.text_input("Mot de passe", type="password")
        bouton_signup = st.button("S'inscrire")
        
        if bouton_signup:
            reponse = signup_request(email, new_user, new_pass)
            
            if reponse and reponse.status_code == 200:
                st.success("Compte cree ! Vous pouvez vous connecter.")
            elif reponse and reponse.status_code == 400:
                st.error("Cet email existe deja.")
            else:
                st.error("Erreur lors de l'inscription.")


else:
    profil = get_user_profile(st.session_state['token'])
    
    if profil and profil.status_code == 200:
        infos = profil.json()
        st.write(f"Bonjour {infos['username']} !")
    
    if st.sidebar.button("Se deconnecter"):
        st.session_state['token'] = None
        st.rerun()
    
    st.write("---")
    st.write("Bienvenue sur votre espace.")
    st.write("(Ici nous ajouterons la recherche d'articles plus tard)")