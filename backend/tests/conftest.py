import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base
from app.api.deps import get_db

from app.models.user import User
from app.models.article import Article
from app.models.quiz import Quiz, Attempt
from app.models.action import Action

from app.services.llm.groq_client import groq_service
from app.services.llm.gemini_client import gemini_service


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)




@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()




@pytest.fixture
def mock_groq():
    with patch.object(groq_service, "generate_summary") as mock_method:
        mock_method.return_value = "Résumé simulé par Groq (Test)\n- Point 1\n- Point 2"
        yield mock_method



@pytest.fixture
def mock_gemini():
    with patch.object(gemini_service, "translate_article") as mock_trans, \
        patch.object(gemini_service, "generate_quiz") as mock_quiz:
        
        mock_trans.return_value = "Traduction simulée par Gemini (Test)"
        
        mock_quiz.return_value = [
            {
                "id": 1,
                "question": "Question Test Gemini ?",
                "options": ["Choix A", "Choix B", "Choix C", "Choix D"],
                "correct_index": 0
            },
            {
                "id": 2,
                "question": "Question Test Gemini 2 ?",
                "options": ["Vrai", "Faux", "Peut-être", "Autre"],
                "correct_index": 1
            }
        ]
        
        class GeminiMockContainer:
            translate_article = mock_trans
            generate_quiz = mock_quiz
            
        yield GeminiMockContainer()