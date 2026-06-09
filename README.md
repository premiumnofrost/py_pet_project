# FastAPI + PostgreSQL + SQLAlchemy + Alembic (Accounts System)

Учебный backend-проект для изучения разработки REST API на Python.

Проект реализует систему пользователей и банковских аккаунтов с операциями над балансом.

---

## 🚀 Стек

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Uvicorn
- Pydantic

---

## 📦 Возможности

### Пользователи
- Создание пользователя
- Получение списка пользователей
- Получение пользователя по ID
- Обновление пользователя
- Удаление пользователя

### Аккаунты
- Создание аккаунта пользователя
- Получение аккаунта по ID
- Получение всех аккаунтов пользователя
- Пополнение баланса (deposit)
- Списание баланса (withdraw)
- Перевод между аккаунтами (transfer)

---

## 🏗 Архитектура

Проект разделён на слои:

- API (FastAPI routers)
- Services (бизнес-логика)
- Models (SQLAlchemy ORM)
- Schemas (Pydantic)
- DB (подключение и сессии)

---

## 📁 Структура

py_pet_project/
│
├── app/
│   ├── api/
│   │   ├── users.py
│   │   └── accounts.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── account.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── account.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   └── account_service.py
│   │
│   └── main.py
│
├── alembic/
├── alembic.ini
└── requirements.txt

---

## ⚙️ Установка

git clone https://github.com/premiumnofrost/py_pet_project.git
cd py_pet_project

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt

---

## 🐘 PostgreSQL

CREATE DATABASE fastapi_db;

---

## 🔧 Настройка

app/db/database.py

DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/fastapi_db"

---

## 📊 Миграции

alembic revision --autogenerate -m "init"
alembic upgrade head
alembic downgrade -1

---

## ▶️ Запуск

uvicorn app.main:app --reload

http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

---

## 👤 Users API

POST /users
{
  "username": "timur",
  "age": 22,
  "email": "timur@mail.com",
  "is_admin": false
}

GET /users
GET /users/{id}

---

## 💰 Accounts API

POST /accounts
{
  "user_id": 1
}

GET /accounts/{id}

POST /accounts/{id}/deposit
{
  "amount": 100
}

POST /accounts/{id}/withdraw
{
  "amount": 50
}

POST /accounts/transfer
{
  "from_account": 1,
  "to_account": 2,
  "amount": 100
}

---

## 🧠 Модели

User:
- id
- username
- email
- age
- is_admin

Account:
- id
- user_id
- balance

---

## 📌 Планы

- JWT authentication
- Password hashing
- Roles system
- Transaction history (ledger)
- Docker
- Tests
- CI/CD