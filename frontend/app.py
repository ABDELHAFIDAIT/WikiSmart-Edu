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
    st.sidebar.write(f"Utilisateur : {get_user_profile(st.session_state['token']).json()['username']}")    
    
    menu = st.sidebar.radio("Navigation", ["Espace de Travail", "Historique"])
    
    if st.sidebar.button("Se deconnecter"):
        st.session_state['token'] = None
        st.rerun()

    
    if menu == "Espace de Travail":
        st.header("Espace de Travail")
        
        source_type = st.radio("Source du contenu :", ["Wikipédia", "Fichier PDF"], horizontal=True)
        
        if source_type == "Wikipédia":
            search_query = st.text_input("Sujet Wikipédia :")
            if st.button("Chercher"):
                if search_query:
                    from utils import search_wiki
                    with st.spinner("Recherche..."):
                        res = search_wiki(st.session_state['token'], search_query)
                        if res and res.status_code == 200:
                            st.session_state['current_article'] = res.json()
                            for key in ['current_summary', 'current_translation', 'current_quiz', 'quiz_result']:
                                if key in st.session_state: del st.session_state[key]
                            st.rerun()
                        else:
                            st.error("Article non trouve.")

        elif source_type == "Fichier PDF":
            uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf")
            
            if uploaded_file is not None:
                if st.button("Envoyer et Analyser"):
                    from utils import upload_pdf_request
                    with st.spinner("Extraction du texte..."):
                        res = upload_pdf_request(st.session_state['token'], uploaded_file)
                        
                        if res and res.status_code == 200:
                            st.session_state['current_article'] = res.json()
                            # Reset des etats
                            for key in ['current_summary', 'current_translation', 'current_quiz', 'quiz_result']:
                                if key in st.session_state: del st.session_state[key]
                            st.success("PDF charge avec succes !")
                            st.rerun()
                        else:
                            st.error("Erreur lors de l'upload.")

        
        if 'current_article' in st.session_state:
            art = st.session_state['current_article']
            st.write("---")
            st.subheader(art['title'])
            st.write(art['content'][:1000] + "...")
            
            
            if st.button("Generer Resume"):
                from utils import generate_summary_request
                res = generate_summary_request(st.session_state['token'], art['id'])
                if res and res.status_code == 200:
                    st.session_state['current_summary'] = res.json()['result']
            
            if 'current_summary' in st.session_state:
                st.info(st.session_state['current_summary'])

            
            langue = st.selectbox("Langue", ["Anglais", "Arabe", "Espagnol"])
            if st.button("Traduire"):
                from utils import translate_article_request
                res = translate_article_request(st.session_state['token'], art['id'], langue)
                if res and res.status_code == 200:
                    st.session_state['current_translation'] = res.json()['result']
            
            if 'current_translation' in st.session_state:
                st.info(st.session_state['current_translation'])

            
            if st.button("Generer Quiz"):
                from utils import generate_quiz_request
                res = generate_quiz_request(st.session_state['token'], art['id'])
                if res and res.status_code == 200:
                    st.session_state['current_quiz'] = res.json()
                    if 'quiz_result' in st.session_state: del st.session_state['quiz_result']
            
            if 'current_quiz' in st.session_state:
                quiz = st.session_state['current_quiz']
                with st.form("quiz"):
                    reponses = []
                    for q in quiz['questions']:
                        st.write(q['question'])
                        choix = st.radio("Choix", q['options'], key=q['id'])
                        reponses.append(q['options'].index(choix))
                    
                    if st.form_submit_button("Valider"):
                        from utils import submit_quiz_request
                        res = submit_quiz_request(st.session_state['token'], quiz['quiz_id'], reponses)
                        if res and res.status_code == 200:
                            st.success(f"Score: {res.json()['score']}%")

    
    elif menu == "Historique":
        st.header("Mes Articles")
        
        from utils import get_history_articles, get_full_article
        res = get_history_articles(st.session_state['token'])
        
        if res and res.status_code == 200:
            articles = res.json()
            for a in articles:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{a['title']}** ({a['created_at'][:10]})")
                with col2:
                    if st.button("Charger", key=a['id']):
                        
                        full_res = get_full_article(st.session_state['token'], a['id'])
                        if full_res and full_res.status_code == 200:
                            st.session_state['current_article'] = full_res.json()
                            
                            for key in ['current_summary', 'current_translation', 'current_quiz', 'quiz_result']:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.success("Article charge ! Retournez dans l'Espace de Travail.")
        else:
            st.warning("Aucun historique.")