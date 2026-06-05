from pydantic import BaseModel, ConfigDict


# --- Pydantic схемы ---
class UserIn(BaseModel):
    username: str
    age: int
    email: str
    is_admin: bool = False


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    age: int
    email: str
    is_admin: bool
