import asyncio
import httpx
import time
import random

# URL твоего запущенного локально FastAPI
BASE_URL = "http://127.0.0.1:8000/users"

async def simulate_user_flow(user_id: int, client: httpx.AsyncClient):
    """Имитирует поведение одного жесткого юзера"""
    payload = {
        "username": f"stress_user_{user_id}_{random.randint(1000, 9999)}",
        "email": f"stress_{user_id}_{random.randint(1000, 9999)}@test.com",
        "password": "supersecretpassword123"
    }
    
    try:
        # 1. Шаг: Создаем юзера (Проверяем POST -> Сервис -> Asyncpg -> Kafka)
        start_time = time.time()
        response = await client.post("", json=payload)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            created_user = response.json()
            user_db_id = created_user.get("id")
            print(f"✅ [Юзер {user_id}] Успешно создан за {latency:.3f} сек. ID в базе: {user_db_id}")
            
            # Немного ждем (типа юзер тупит в интерфейсе)
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            # 2. Шаг: Активируем/Меняем статус юзера (Проверяем PATCH)
            status_payload = {"is_active": True}
            await client.patch(f"/{user_db_id}/status", json=status_payload)
            
            # 3. Шаг: Стучимся в аккаунты (Проверяем GET)
            await client.get(f"/{user_db_id}/accounts")
            
        else:
            print(f"❌ [Юзер {user_id}] Ошибка создания! Код: {response.status_code}, Ответ: {response.text}")
            
    except Exception as e:
        print(f"💥 [Юзер {user_id}] Сервер не ответил или упал с ошибкой: {e}")

async def run_stress_test(total_users: int):
    print(f"🔥 Начинаем стресс-тест! Спавним {total_users} асинхронных юзеров одновременно...")
    start_time = time.time()
    
    # Открываем один асинхронный клиент с большими таймаутами
    limits = httpx.Limits(max_keepalive_connections=total_users, max_connections=total_users)
    async with httpx.AsyncClient(base_url=BASE_URL, limits=limits, timeout=10.0) as client:
        
        # Создаем пачку задач для Event Loop
        tasks = [simulate_user_flow(i, client) for i in range(total_users)]
        
        # Бахаем их ВСЕ ОДНОВРЕМЕННО
        await asyncio.gather(*tasks)

    total_time = time.time() - start_time
    print(f"\n🏁 Стресс-тест окончен!")
    print(f"⏱️ Обработано {total_users} комплексных сценариев за {total_time:.2f} сек.")
    print(f"🚀 Средняя скорость сервера: {total_users / total_time:.1f} пользователей в секунду!")

if __name__ == "__main__":
    # Задаем количество одновременных запросов (начни с 50, потом подними до 150-200)
    CONCURRENT_USERS = 100
    asyncio.run(run_stress_test(CONCURRENT_USERS))