from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.user import User


class AccountService:
    # ---------------- CREATE ----------------
        @staticmethod
        def create_account(db: Session, user_id: int):
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raise ValueError("User not found")
            
            account = Account(
                user_id=user_id
            )

            db.add(account)
            db.commit()
            db.refresh(account)

            return account
        
    # ---------------- get acc ----------------
        @staticmethod
        def get_user_by_account_id(db: Session, account_id: int):
            account = db.query(Account).filter(Account.id == account_id).first()
            if not account:
                raise HTTPException(status_code=404, detail="User not found")

            return account.user

    # ---------------- get User of this Account ----------------
        @staticmethod
        def get_user_account(db: Session, account_id: int):
            return db.query(User).filter(User.id == account_id).first()


    # ---------------- deposit ----------------
        @staticmethod
        def deposit(db: Session, account_id: int, amount: int):
            account = db.query(Account).filter(Account.id == account_id).first()
            if not account:
                return None

            account.balance += amount

            db.commit()
            db.refresh(account)
            return account

    # ---------------- withdraw ----------------
        @staticmethod
        def withdraw(db: Session, account_id: int, amount: int):
            account = db.query(Account).filter(Account.id == account_id).first()
            if not account:
                return None

            if account.balance < amount:
                raise ValueError("Not enough balance")

            account.balance -= amount

            db.commit()
            db.refresh(account)
            return account

    # ---------------- transfer ----------------
        @staticmethod
        def transfer(db: Session, from_id: int, to_id: int, amount: int):
            from_acc = db.query(Account).filter(Account.user_id == from_id).first()
            to_acc = db.query(Account).filter(Account.user_id == to_id).first()

            if not from_acc or not to_acc:
                raise ValueError("Not find Account")

            if from_acc.balance < amount:
                raise ValueError("Not enough balance")

            from_acc.balance -= amount
            to_acc.balance += amount

            db.commit()
            db.refresh(from_acc)
            db.refresh(to_acc)

            return {"from": from_acc, "to": to_acc}