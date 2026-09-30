import json, os, time, urllib.request
from windows_agent.agent import open_app, open_website, find_file

CORE=os.getenv("RED_CORE_URL","").rstrip("/")
TOKEN=os.getenv("RED_AGENT_TOKEN","")

def request(path,method="GET",payload=None):
    data=None if payload is None else json.dumps(payload).encode()
    req=urllib.request.Request(CORE+path,data=data,method=method,
        headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read())

def execute(cmd):
    a=cmd["action"];args=cmd.get("args",{})
    if a=="open_app":return open_app(args.get("name",""))
    if a=="open_website":return open_website(args.get("url",""))
    if a=="find_file":return {"ok":True,"matches":find_file(args.get("name",""))}
    return {"ok":False,"error":"Action not allow-listed"}

def run():
    if not CORE or not TOKEN: raise RuntimeError("Set RED_CORE_URL and RED_AGENT_TOKEN")
    print("Red Windows Agent connected.")
    while True:
        try:
            cmd=request("/api/device/next")
            if cmd.get("command"):
                result=execute(cmd["command"])
                request("/api/device/complete","POST",{"id":cmd["command"]["id"],"result":result})
        except Exception as e: print("Connection:",e)
        time.sleep(3)

if __name__=="__main__":run()
