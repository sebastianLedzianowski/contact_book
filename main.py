from fastapi import FastAPI

from src.routes import contact

app = FastAPI()

app.include_router(contact.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}