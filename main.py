import redis.asyncio as redis
import uvicorn

from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter.depends import RateLimiter

from src.routes import contacts, auth, users

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

rate_limit = RateLimiter(times=10, seconds=60)

@app.on_event("startup")
async def startup():
    """
    Function to initialize FastAPILimiter on application startup.
    """
    r = await redis.Redis(host=os.getenv("REDIS_HOST"),
                          port=int(os.getenv("REDIS_PORT")),
                          db=int(os.getenv("REDIS_DB")),
                          encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", dependencies=[Depends(rate_limit)])
async def read_root():
    """
    Root endpoint of the application.
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)