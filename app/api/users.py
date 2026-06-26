from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession  # Меняем импорт на асинхронный

from app.db.database import get_db
from app.schemas.user import UserIn, UserOut, UserStatus, UserPatch
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------- CREATE ----------------
@router.post("", response_model=UserOut)
async def create_user(user: UserIn, db: AsyncSession = Depends(get_db)):
    # Ждем пока сервис создаст юзера и отправит ивент в Кафку
    return await UserService.create_user(db, user)


# ---------------- READ ALL ----------------
@router.get("", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return await UserService.list_users(db, limit=limit, offset=offset)


# ---------------- READ ONE ----------------
@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------------- PATCH (UPDATE) ----------------
@router.put("/{user_id}", response_model=UserPatch)
async def update_user(user_id: int, user_data: UserPatch, db: AsyncSession = Depends(get_db)):
    user = await UserService.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------------- USER ACCOUNTS (READ ONLY) ----------------
@router.get("/{user_id}/accounts")
async def get_user_accounts(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.get_user_accounts(db, user_id)


# ---------------- SET USER STATUS ----------------
@router.patch("/{user_id}/status")
async def set_user_status(user_id: int, data: UserStatus, db: AsyncSession = Depends(get_db)):
    user = await UserService.set_active(db, user_id, data.is_active)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ---------------- DELETE ----------------
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}