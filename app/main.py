import os, hmac
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.red_core import RedCore
from app.monitors import MonitorEngine
from app.tasks import TaskStore
from app.device_queue import DeviceQueue
from app.events import EventStore

app=FastAPI(title="Red AI",version="0.7.0")
red=RedCore();monitors=MonitorEngine(red.attention);tasks=TaskStore();devices=DeviceQueue();events=EventStore()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class Message(BaseModel): text:str
class TaskRequest(BaseModel): text:str; due:str|None=None
class DeviceCommand(BaseModel): action:str; args:dict={}
class DeviceResult(BaseModel): id:str; result:dict

def agent_auth(authorization:str|None):
    expected=os.getenv("RED_AGENT_TOKEN","")
    supplied=(authorization or "").removeprefix("Bearer ")
    if not expected or not hmac.compare_digest(expected,supplied): raise HTTPException(401,"Invalid agent token")

@app.get("/")
def root():return FileResponse("app/static/index.html")
@app.get("/manifest.json")
def manifest():return FileResponse("app/static/manifest.json")
@app.get("/sw.js")
def sw():return FileResponse("app/static/sw.js",media_type="application/javascript")
@app.get("/health")
def health():return {"ok":True,"name":"Red","version":"0.7.0"}
@app.get("/api/diagnostics/reasoning")
def reasoning_diagnostics():return red.reasoning.diagnostics()
@app.post("/api/chat")
def chat(message:Message):return red.handle(message.text)
@app.get("/api/monitors/run")
def run_monitors():return {"events":monitors.run()}
@app.get("/api/tasks")
def list_tasks():return {"tasks":tasks.list()}
@app.post("/api/tasks")
def add_task(task:TaskRequest):return tasks.add(task.text,task.due)
@app.post("/api/device/command")
def command(c:DeviceCommand):return devices.enqueue(c.action,c.args)
@app.get("/api/device/next")
def device_next(authorization:str|None=Header(default=None)):
 agent_auth(authorization);return {"command":devices.next()}
@app.post("/api/device/complete")
def device_complete(r:DeviceResult,authorization:str|None=Header(default=None)):
 agent_auth(authorization);return devices.complete(r.id,r.result)

@app.get("/api/events")
def unread_events():return {"events":events.unread()}

@app.post("/api/events/{event_id}/read")
def read_event(event_id:str):return events.mark_read(event_id) or {"ok":False}
