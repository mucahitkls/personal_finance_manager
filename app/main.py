from fastapi import FastAPI
from app.api.endpoints import user, transaction

app = FastAPI()
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(transaction.router, prefix="/transactions", tags=["transactions"])

