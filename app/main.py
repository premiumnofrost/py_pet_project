from fastapi import FastAPI, Depends, HTTPException

from app.api.users import router as users_router
from app.api.accounts import router as accounts_router

app = FastAPI()


# --- routers ---
app.include_router(users_router)
app.include_router(accounts_router)


# --- healthcheck ---
@app.get("/health")
def health():
    return {"status": "ok"}