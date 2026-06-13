from app.models.account import Account
from app.services.account_service import AccountService


def test_deposit_success(db):
    # 1. Создаем аккаунт
    new_acc = Account(id=1, user_id=1, balance=100)
    db.add(new_acc)
    db.commit()
    
    # 2. Делаем депозит
    AccountService.deposit(db, account_id=1, amount=50)
    
    # 3. Проверяем
    db.refresh(new_acc)
    assert new_acc.balance == 150