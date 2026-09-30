from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.red_core import RedCore
from app.monitors import MonitorEngine
from app.tasks import TaskStore

app = FastAPI(title="Red AI", version="0.4.0")
red = RedCore()
monitors = MonitorEngine(red.attention)
tasks = TaskStore()

class Message(BaseModel):
    text: str

class TaskRequest(BaseModel):
    text: str
    due: str | None = None

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/health")
def health():
    return {"ok": True, "name": "Red", "version": "0.4.0"}

@app.post("/api/chat")
def chat(message: Message):
    return red.handle(message.text)

@app.get("/api/monitors/run")
def run_monitors():
    return {"events": monitors.run()}

@app.get("/api/tasks")
def list_tasks():
    return {"tasks": tasks.list()}

@app.post("/api/tasks")
def add_task(task: TaskRequest):
    return tasks.add(task.text, task.due)
