from fastapi import FastAPI
from pydantic import BaseModel
from app.red_core import RedCore

app = FastAPI(title="Red AI", version="0.1.0")
red = RedCore()

class Message(BaseModel):
    text: str

@app.get("/")
def root():
    return {"name": "Red", "version": "0.1.0", "status": "online"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/chat")
def chat(message: Message):
    return red.handle(message.text)
