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
    
    menu = st.sidebar.radio("Navigation", ["Espace de Travail", "Historique", "Profil"])
    
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
        st.header("Mes Articles et Scores")
        
        from utils import get_history_articles, get_full_article, get_article_quizzes_request, get_quiz_attempts_request
        res = get_history_articles(st.session_state['token'])
        
        if res and res.status_code == 200:
            articles = res.json()
            
            for a in articles:
                with st.expander(f"{a['title']} ({a['created_at'][:10]})"):
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        if st.button("Travailler dessus", key=f"load_{a['id']}"):
                            full_res = get_full_article(st.session_state['token'], a['id'])
                            if full_res and full_res.status_code == 200:
                                st.session_state['current_article'] = full_res.json()
                                for key in ['current_summary', 'current_translation', 'current_quiz', 'quiz_result']:
                                    if key in st.session_state: del st.session_state[key]
                                st.success("Chargé ! Allez dans 'Espace de Travail'")

                    with col2:
                        st.caption("Historique des Quiz")
                        quizzes_res = get_article_quizzes_request(st.session_state['token'], a['id'])
                        
                        if quizzes_res and quizzes_res.status_code == 200:
                            quizzes = quizzes_res.json()
                            if not quizzes:
                                st.write("Aucun quiz généré.")
                            
                            for q in quizzes:
                                attempts_res = get_quiz_attempts_request(st.session_state['token'], q['id'])
                                if attempts_res and attempts_res.status_code == 200:
                                    attempts = attempts_res.json()
                                    if attempts:
                                        for attempt in attempts:
                                            st.write(f"- Quiz du {q['created_at'][:10]} : **{attempt['score']}%**")
                                    else:
                                        st.write(f"- Quiz du {q['created_at'][:10]} : Pas encore tenté")
                        else:
                            st.write("Erreur chargement quiz.")

        else:
            st.warning("Vous n'avez pas encore d'historique.")
    
    
    elif menu == "Profil":
        st.header("Mon Profil")
        
        from utils import get_user_profile
        profil_req = get_user_profile(st.session_state['token'])
        
        if profil_req and profil_req.status_code == 200:
            infos = profil_req.json()
            
            st.write(f"**Nom d'utilisateur :** {infos['username']}")
            st.write(f"**Email :** {infos['email']}")
            st.write(f"**Rôle :** {infos['role']}")
            
            st.write("---")
            st.subheader("Changer de mot de passe")
            
            with st.form("password_change"):
                old_pass = st.text_input("Ancien mot de passe", type="password")
                new_pass = st.text_input("Nouveau mot de passe", type="password")
                bouton_mdp = st.form_submit_button("Mettre à jour")
                
                if bouton_mdp:
                    from utils import update_password_request
                    res = update_password_request(st.session_state['token'], old_pass, new_pass)
                    
                    if res and res.status_code == 200:
                        st.success("Mot de passe modifié avec succès !")
                    elif res and res.status_code == 400:
                        st.error("Erreur : Ancien mot de passe incorrect.")
                    else:
                        st.error("Erreur technique.")
        else:
            st.error("Impossible de charger les informations du profil.")