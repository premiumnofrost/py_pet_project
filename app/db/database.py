from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# формат: postgresql://пользователь:пароль@хост:порт/имя_базы
DATABASE_URL = "postgresql://postgres:@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()