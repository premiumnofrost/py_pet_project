from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.user import User
from app.models.account import Account

from app.services.kafka_producer import kafka_service 

class UserService:
    # ---------------- CREATE ----------------
    @staticmethod
    async def create_user(db: AsyncSession, user_data):
        user = User(**user_data.model_dump())
        db.add(user)

        await db.commit()
        await db.refresh(user)

        event_data = {
            "event_type": "user_created",
            "user_id": user.id,
            "email": user.email,
            "is_active": user.is_active
        }
        try:
            await kafka_service.send_message("user_events", event_data)
        except Exception as e:
            print(f"[Kafka Error] Failed to send user_created event: {e}")

        return user

    # ---------------- GET ONE ----------------
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    # ---------------- LIST ----------------
    @staticmethod
    async def list_users(db: AsyncSession, limit: int = 10, offset: int = 0):
        stmt = select(User).offset(offset).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    # ---------------- UPDATE FULL ----------------
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_data):
        update_data = user_data.model_dump(exclude_unset=True)

        if not update_data:
            return None

        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
            .returning(User)
        )

        result = await db.execute(stmt)
        await db.commit()

        user_row = result.fetchone()

        if user_row:
            event_data = {
                "event_type": "user_updated",
                "user_id": user_id,
                "updated_fields": list(update_data.keys())
            }
            try:
                await kafka_service.send_message("user_events", event_data)
            except Exception as e:
                print(f"[Kafka Error] Failed to send user_updated event: {e}")

        return user_row

    # ---------------- Active ----------------
    @staticmethod
    async def set_active(db: AsyncSession, user_id: int, is_active: bool):
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        
        if not user:
            return None

        user.is_active = is_active

        await db.commit()
        await db.refresh(user)

        event_data = {
            "event_type": "user_status_changed",
            "user_id": user.id,
            "is_active": user.is_active
        }
        try:
            await kafka_service.send_message("user_events", event_data)
        except Exception as e:
            print(f"[Kafka Error] Failed to send user_status_changed event: {e}")

        return user

    # ---------------- GET USER ACCOUNTS ----------------
    @staticmethod
    async def get_user_accounts(db: AsyncSession, user_id: int):
        stmt = select(Account).where(Account.user_id == user_id)
        result = await db.execute(stmt)
        accounts = result.scalars().all()
        
        if not accounts:
            return False
        return accounts

    # ---------------- DELETE ----------------
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        
        if not user:
            return False

        await db.delete(user)
        await db.commit()

        # Отправляем отчетное событие об удалении
        event_data = {
            "event_type": "user_deleted",
            "user_id": user_id
        }
        try:
            await kafka_service.send_message("user_events", event_data)
        except Exception as e:
            print(f"[Kafka Error] Failed to send user_deleted event: {e}")

        return True