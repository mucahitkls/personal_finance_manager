# from fastapi import FastAPI
# from app.api.endpoints import user, transaction
from app.database.database import global_init

global_init()


# app = FastAPI()
# app.include_router(user.router, prefix="/users", tags=["users"])
# app.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
#
