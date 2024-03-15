from fastapi import FastAPI
from database import database
from routes.user import router as user_router
from routes.stocks import router as stock_router
from routes.companies import router as companies_router
import sys
app = FastAPI()
sys.setrecursionlimit(1500)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(stock_router, prefix="/stocks", tags=["Stocks"])
app.include_router(companies_router, prefix="/companies", tags=["Companies"])
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
