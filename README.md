# WikiSmart-Edu
EduSmart est une plateforme éducative intelligente, développée avec FastAPI, PostgreSQL, SQLAlchemy, Pydantic et OAuth 2.0, utilisant un LLM pour résumer, traduire et générer des QCM à partir d’articles Wikipedia, avec vérification d’identité via FaceAPI.

<br>

```bash
wikismart-edu/
├── 📂 backend/                 # Le cœur de l'application FastAPI
│   ├── 📂 app/                 # Code source principal
│   │   ├── 📂 api/             # Routes et Endpoints (Contrôleurs)
│   │   │   ├── __init__.py
│   │   │   ├── deps.py         # Dépendances (ex: get_current_user, check_admin)
│   │   │   └── v1/             # Versionning de l'API
│   │   │       ├── __init__.py
│   │   │       ├── auth.py     # Login, Register, FaceAPI check
│   │   │       ├── users.py    # CRUD User (Admin only)
│   │   │       ├── content.py  # Wiki ingestion, PDF upload
│   │   │       ├── ai_tools.py # Résumé, Traduction, Quiz (LLM endpoints)
│   │   │       └── router.py   # Agrégateur des routeurs
│   │   │
│   │   ├── 📂 core/            # Configuration et Sécurité
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # Pydantic Settings (chargement .env)
│   │   │   ├── database.py     # SessionLocal, Base SQLAlchemy
│   │   │   ├── security.py     # Hachage pwd, JWT logic
│   │   │   ├── logging.py      # Config des logs structurés
│   │   │   └── exceptions.py   # Gestion centralisée des erreurs
│   │   │
│   │   ├── 📂 models/          # Modèles SQLAlchemy (Base de données)
│   │   │   ├── __init__.py
│   │   │   ├── user.py         # Table Users
│   │   │   ├── article.py      # Table Articles
│   │   │   └── quiz.py         # Table QuizAttempts
│   │   │
│   │   ├── 📂 schemas/         # Modèles Pydantic (Validation des données)
│   │   │   ├── __init__.py
│   │   │   ├── user.py         # UserCreate, UserResponse
│   │   │   ├── article.py      # ArticleRequest (URL), ArticleResponse
│   │   │   ├── quiz.py         # QuizGenerated, QuizResult
│   │   │   └── token.py        # Token schema
│   │   │
│   │   ├── 📂 services/        # Logique métier pure (Business Logic)
│   │   │   ├── __init__.py
│   │   │   ├── 📂 ingestion/   # Traitement des sources
│   │   │   │   ├── wikipedia.py # Client Wikipedia (User-Agent, Clean URL)
│   │   │   │   ├── pdf_loader.py # LangChain loader
│   │   │   │   └── cleaner.py   # Regex pour nettoyer/segmenter le texte
│   │   │   │
│   │   │   ├── 📂 llm/         # Intégration IA
│   │   │   │   ├── groq_client.py   # Service Résumé
│   │   │   │   ├── gemini_client.py # Service Traduction & Quiz
│   │   │   │   └── prompts.py       # Stockage des prompts (System prompts)
│   │   │   │
│   │   │   ├── face_auth.py    # Logique FaceAPI
│   │   │   └── exporter.py     # Génération PDF/TXT des résultats
│   │   │
│   │   └── main.py             # Point d'entrée FastAPI
│   │
│   ├── 📂 tests/               # Tests automatisés (Pytest)
│   │   ├── __init__.py
│   │   ├── conftest.py         # Fixtures (DB test, Client test)
│   │   ├── mocks/              # Fichiers JSON ou classes pour mocker les LLMs
│   │   ├── test_auth.py
│   │   ├── test_ingestion.py
│   │   └── test_llm_integration.py
│   │
│   ├── .env                    # Variables d'environnement (API Keys, DB URL)
│   ├── .dockerignore
│   ├── Dockerfile              # Image Docker pour le Backend
│   ├── alembic.ini             # Config migrations BDD
│   ├── pyproject.toml          # Dépendances (Poetry) ou requirements.txt
│   └── migrations/             # Dossier généré par Alembic
│
├── 📂 frontend/                # Interface Utilisateur (ex: Streamlit)
│   ├── .streamlit/             # Config Streamlit (theme, etc.)
│   ├── components/             # Composants UI réutilisables (Sidebar, QuizCard)
│   ├── pages/                  # Pages multipages (Login, Dashboard, History)
│   ├── utils/                  # Appels API vers le backend (requests)
│   ├── app.py                  # Point d'entrée Frontend
│   └── Dockerfile              # Image Docker pour le Frontend
│
├── docker-compose.yml          # Orchestration (Backend + DB + Frontend)
└── README.md                   # Documentation du projet
```