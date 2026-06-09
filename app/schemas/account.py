from pydantic import BaseModel, ConfigDict


class AccountIn(BaseModel):
    user_id: int


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    balance: int

class BalanceOperation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: int

class TransferById(BaseModel):   
    model_config = ConfigDict(from_attributes=True)

    from_account: int
    to_account: int   
    amount: int