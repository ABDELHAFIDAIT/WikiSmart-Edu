import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
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



SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="function")
def db_session() :
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try :
        yield session
    finally :
        session.close()
        Base.metadata.drop_all(bind=engine)
        
        
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear() 




@pytest.fixture
def mock_groq():
    with patch("app.services.llm.groq_client.groq_service") as mock:
        mock.generate_summary.return_value = (
            "Ceci est un résumé simulé par un test.\n"
            "- Point clé 1\n"
            "- Point clé 2"
        )
        yield mock
        
        


@pytest.fixture
def mock_gemini():
    with patch("app.services.llm.gemini_client.gemini_service") as mock:
        mock.translate_article.return_value = "Ceci est une traduction simulée (Mock)."
        
        mock.generate_quiz.return_value = [
            {
                "id": 1,
                "question": "Question Test 1 ?",
                "options": ["A", "B", "C", "D"],
                "correct_index": 0
            },
            {
                "id": 2,
                "question": "Question Test 2 ?",
                "options": ["X", "Y", "Z", "W"],
                "correct_index": 1
            }
        ]
        yield mock