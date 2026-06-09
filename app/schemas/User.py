from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- Pydantic схемы ---
class UserIn(BaseModel):
    username: str
    age: int
    email: str
    is_admin: bool = False
    is_active: bool

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    age: int
    email: str
    is_admin: bool
    is_active: bool

class UserStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_active: bool


class UserPatch(BaseModel):
    
    username: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

