from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
# from sqlalchemy.exc import SQLAlchemyError

from app.models.account import Account
from app.models.user import User
from app.services.kafka_producer import kafka_service


class AccountService:
    # ---------------- CREATE ----------------
    @staticmethod
    async def create_account(db: AsyncSession, user_id: int):

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            raise ValueError("User not found")
        
        account = Account(user_id=user_id)

        db.add(account)
        await db.commit()
        await db.refresh(account)

        return account
        
    # ---------------- get acc ----------------
    @staticmethod
    async def get_user_by_account_id(db: AsyncSession, account_id: int):
        result = await db.execute(select(Account).where(Account.id == account_id))
        account = result.scalars().first()
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        return account.user

    # ---------------- get User of this Account ----------------
    @staticmethod
    async def get_user_account(db: AsyncSession, account_id: int):
        result = await db.execute(select(User).where(User.id == account_id))
        return result.scalars().first()

    # ---------------- deposit ----------------
    @staticmethod
    async def deposit(db: AsyncSession, account_id: int, amount: int):

        stmt = select(Account).where(Account.id == account_id).with_for_update()
        result = await db.execute(stmt)
        account = result.scalars().first()
        
        if not account:
            return None 
        
        account.balance += amount

        await db.commit()
        await db.refresh(account)
        
        try:
            await kafka_service.send_message("account_events", {
                "event_type": "deposit",
                "account_id": account_id,
                "amount": amount,
                "new_balance": account.balance
            })
        except Exception as e:
            print(f"[Kafka Error] Failed to send user_deleted event: {e}")
