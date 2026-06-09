from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.account import (
    AccountIn,
    AccountOut,
    BalanceOperation,
    TransferById
)
from app.services.account_service import AccountService

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


# ---------- CREATE ACCOUNT ----------
@router.post("", response_model=AccountIn)
def create_account(
    data: AccountIn,
    db: Session = Depends(get_db)
):
    return AccountService.create_account(db, data.user_id)


# ---------- GET ACCOUNT ----------
@router.get("/{account_id}", response_model=AccountOut)
def get_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    account = AccountService.get_account(db, account_id)

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return account


# ---------- GET ALL ACCOUNTS ----------
@router.get("/user/{user_id}", response_model=list[AccountOut])
def get_user_accounts(user_id: int, db: Session = Depends(get_db)):
    return AccountService.get_user_accounts(db, user_id)



# ---------- DEPOSIT ----------
@router.post("/{account_id}/deposit")
def deposit(
    account_id: int,
    data: BalanceOperation,
    db: Session = Depends(get_db)
):
    account = AccountService.deposit(
        db,
        account_id,
        data.amount
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return account


# ---------- WITHDRAW ----------
@router.post("/{account_id}/withdraw")
def withdraw(
    account_id: int,
    data: BalanceOperation,
    db: Session = Depends(get_db)
):
    account = AccountService.withdraw(
        db,
        account_id,
        data.amount
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return account


# ---------- TRANSFER ----------
@router.post("/transfer")
def transfer(
    data: TransferById,
    db: Session = Depends(get_db)
):
    return AccountService.transfer(
        db,
        data.from_account,
        data.to_account,
        data.amount
    )