# FastAPI + PostgreSQL + SQLAlchemy + Alembic

Учебный pet-проект для изучения backend-разработки на Python.

## Стек

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Uvicorn

---

## Возможности

### Пользователи

- Создание пользователя
- Получение списка пользователей
- Получение пользователя по ID

---

## Структура проекта

```text
py_pet_project/
│
├── app/
│   ├── api/
│   │   └── users.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── user.py
│   │
│   └── main.py
│
├── alembic/
│
├── alembic.ini
│
└── requirements.txt
```

---

## Установка

### 1. Клонировать проект

```bash
git clone https://github.com/premiumnofrost/py_pet_project.git
cd py_pet_project
```

### 2. Создать виртуальное окружение

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/Mac:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

## PostgreSQL

Создать базу данных:

```sql
CREATE DATABASE fastapi_db;
```

---

## Настройка подключения

Файл:

```python
app/db/database.py
```

Изменить строку подключения:

```python
DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/fastapi_db"
```

---

## Миграции

Создание миграции:

```bash
alembic revision --autogenerate -m "init"
```

Применение миграций:

```bash
alembic upgrade head
```

Откат на одну миграцию:

```bash
alembic downgrade -1
```

---

## Запуск проекта

```bash
uvicorn app.main:app --reload
```

После запуска:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## API

### Создать пользователя

POST

```http
/users
```

Пример запроса:

```json
{
  "username": "timur",
  "age": 22,
  "email": "timur@mail.com",
  "is_admin": false
}
```

---

### Получить список пользователей

GET

```http
/users
```

---

### Получить пользователя по ID

GET

```http
/users/{id}
```

Пример:

```http
/users/1
```

---

## Модель User

```python
class User(Base):
    __tablename__ = "users"

    id: int
    username: str
    age: int
    email: str
    is_admin: bool
```

---

## Планы по развитию проекта

- [ ] Update User
- [ ] Delete User
- [ ] JWT Authentication
- [ ] Регистрация пользователей
- [ ] Хеширование паролей
- [ ] Роли пользователей
- [ ] Docker
- [ ] Тесты (pytest)
- [ ] CI/CD
