from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserIn, UserOut, UserStatus, UserPatch
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------- CREATE ----------------
@router.post("", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)


# ---------------- READ ALL ----------------
@router.get("", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return UserService.list_users(db, limit=limit, offset=offset)


# ---------------- READ ONE ----------------
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------------- PATCH ----------------
@router.put("/{user_id}", response_model=UserPatch)
def update_user(user_id: int, user_data: UserPatch, db: Session = Depends(get_db)):
    user = UserService.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ---------------- USER ACCOUNTS (READ ONLY) ----------------
@router.get("/{user_id}/accounts")
def get_user_accounts(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user_accounts(db, user_id)


# ----------------SET USER STATUS ----------------
@router.patch("/{user_id}/status")
def set_user_status(user_id: int, data:UserStatus, db: Session = Depends(get_db)):
    user = UserService.set_active(db, user_id, data.is_active)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# ---------------- DELETE ----------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
