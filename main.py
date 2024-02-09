import redis.asyncio as redis

from fastapi import FastAPI, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth

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

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=os.getenv("REDIS_HOST"),
                          port=int(os.getenv("REDIS_PORT")),
                          db=int(os.getenv("REDIS_DB")),
                          encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.exception_handler(HTTPException)
async def exception_limit_handling(request, exc):
    if exc.status_code == 429:
        return JSONResponse(content={"detail": "Too many requests, no more than 10 per minute."},
                            status_code=429)
    return exc