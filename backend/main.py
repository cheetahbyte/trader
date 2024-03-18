from fastapi import FastAPI, Request
from database import database
from routes.user import router as user_router
from fastapi.middleware.gzip import GZipMiddleware
from routes.stocks import router as stock_router
from routes.companies import router as companies_router
import sys, time

app = FastAPI()
sys.setrecursionlimit(1500)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(stock_router, prefix="/stocks", tags=["Stocks"])
app.include_router(companies_router, prefix="/companies", tags=["Companies"])

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
