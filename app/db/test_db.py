from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv

load_dotenv() # Загружаем .env
url = os.getenv("DATABASE_URL")

engine = create_engine(url)
inspector = inspect(engine)

print(f"Подключаюсь к: {url}")
print(f"Таблицы в базе: {inspector.get_table_names()}")