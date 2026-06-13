import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Импортируй свой Base и модели
from app.db.database import Base

# Это движок для тестов
engine = create_engine("sqlite:///:memory:") 
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    # Создаем таблицы в памяти перед каждым тестом
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    # Чистим после теста
    session.close()
    Base.metadata.drop_all(bind=engine)