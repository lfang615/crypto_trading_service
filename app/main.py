from fastapi import FastAPI
from app.api.endpoints import auth, order


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(order.router, prefix="/order", tags=["orders"])