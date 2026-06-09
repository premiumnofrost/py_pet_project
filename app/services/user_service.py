from sqlalchemy.orm import Session
from app.models.user import User
from app.models.account import Account

from sqlalchemy import update

class UserService:
    # ---------------- CREATE ----------------
    @staticmethod
    def create_user(db: Session, user_data):
        user = User(**user_data.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # ---------------- GET ONE ----------------
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # ---------------- LIST ----------------
    @staticmethod
    def list_users(db: Session, limit: int = 10, offset: int = 0):
        return db.query(User).offset(offset).limit(limit).all()

    # ---------------- UPDATE FULL ----------------
    @staticmethod
    def update_user(db: Session, user_id: int, user_data):
        update_data = user_data.model_dump(exclude_unset=True)

        if not update_data:
            return None

        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
            .returning(User)
        )

        result = db.execute(stmt)
        db.commit()

        return result.fetchone()
    # ---------------- Active ----------------

    @staticmethod
    def set_active(db: Session, user_id: int, is_active: bool):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        user.is_active = is_active

        db.commit()
        db.refresh(user)
        return user

    # ---------------- GET USER ACCOUTS ----------------
    @staticmethod
    def get_user_accounts(db: Session, user_id: int):
        account = db.query(Account).filter(Account.user_id == user_id).all()
        if not account:
            return False
        return account

    # ---------------- DELETE ----------------
    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True
    