from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine
from app.services.kafka_producer import kafka_service

from app.api.users import router as users_router
from app.api.accounts import router as accounts_router



@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Запуск Kafka...")
    await kafka_service.start()
    
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        raise e 
    
    yield
    
    print("🛑 Остановка сервисов...")
    await kafka_service.stop()
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# --- routers ---
app.include_router(users_router)
app.include_router(accounts_router)

# --- healthcheck ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/send")
async def send_event(data: dict):
    await kafka_service.send_message("my_topic", data)
    return {"status": "ok"}