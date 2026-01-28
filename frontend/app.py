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
    

    st.subheader("Rechercher un article")
    search_query = st.text_input("Sujet Wikipédia :")
    
    if st.button("Chercher"):
        if search_query:
            from utils import search_wiki
            with st.spinner("Recherche en cours..."):
                res = search_wiki(st.session_state['token'], search_query)
                
                if res and res.status_code == 200:
                    article = res.json()
                    st.session_state['current_article'] = article
                    st.success(f"Article trouvé : {article['title']}")
                elif res and res.status_code == 404:
                    st.warning("Aucun article trouvé.")
                else:
                    st.error("Erreur lors de la recherche.")


    if 'current_article' in st.session_state:
        art = st.session_state['current_article']
        st.write("---")
        st.header(art['title'])
        st.write(art['content'][:1000] + "...")
        
        st.write("---")
        st.subheader("Outils Intelligence Artificielle")
        
        if st.button("Generer un Resume"):
            from utils import generate_summary_request
            
            with st.spinner("L'IA travaille..."):
                res = generate_summary_request(st.session_state['token'], art['id'])
                
                if res and res.status_code == 200:
                    data = res.json()
                    st.session_state['current_summary'] = data['result']
                else:
                    st.error("Erreur lors de la generation du resume")

        if 'current_summary' in st.session_state:
            st.success("Resume genere avec succes :")
            st.write(st.session_state['current_summary'])