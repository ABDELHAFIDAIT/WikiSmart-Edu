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
        
        
        
        st.write("---")
        st.subheader("Traduire l'article")
        
        langue = st.selectbox("Choisir une langue", ["Anglais", "Arabe", "Espagnol", "Allemand"])
        
        if st.button("Traduire"):
            from utils import translate_article_request
            
            with st.spinner("Traduction en cours..."):
                res = translate_article_request(st.session_state['token'], art['id'], langue)
                
                if res and res.status_code == 200:
                    data = res.json()
                    st.session_state['current_translation'] = data['result']
                else:
                    st.error("Erreur lors de la traduction")

        if 'current_translation' in st.session_state:
            st.success("Traduction :")
            st.write(st.session_state['current_translation'][:1000] + "...")
            
        
        
        
        st.write("---")
        st.subheader("Quiz de connaissances")
        
        if st.button("Generer un Quiz"):
            from utils import generate_quiz_request
            
            with st.spinner("Generation des questions..."):
                res = generate_quiz_request(st.session_state['token'], art['id'])
                
                if res and res.status_code == 200:
                    st.session_state['current_quiz'] = res.json()
                    if 'quiz_result' in st.session_state:
                        del st.session_state['quiz_result']
                else:
                    st.error("Erreur generation quiz")

        if 'current_quiz' in st.session_state:
            quiz_data = st.session_state['current_quiz']
            st.write(f"Questionnaire : {len(quiz_data['questions'])} questions")
            
            with st.form("quiz_form"):
                user_answers_indices = []
                
                for q in quiz_data['questions']:
                    st.write(f"**{q['question']}**")
                    choix = st.radio("Reponse :", q['options'], key=q['id'])
                    index_choix = q['options'].index(choix)
                    user_answers_indices.append(index_choix)
                    st.write("---")
                
                submitted = st.form_submit_button("Valider mes reponses")
                
                if submitted:
                    from utils import submit_quiz_request
                    res = submit_quiz_request(st.session_state['token'], quiz_data['quiz_id'], user_answers_indices)
                    
                    if res and res.status_code == 200:
                        st.session_state['quiz_result'] = res.json()
                    else:
                        st.error("Erreur lors de la correction")

        if 'quiz_result' in st.session_state:
            result = st.session_state['quiz_result']
            st.success(f"Score : {result['score']}%")
            st.info(result['message'])