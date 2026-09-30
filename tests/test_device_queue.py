from app.device_queue import DeviceQueue
def test_queue(tmp_path):
 q=DeviceQueue(str(tmp_path/"q.json"));c=q.enqueue("open_app",{"name":"notepad"})
 assert q.next()["id"]==c["id"];q.complete(c["id"],{"ok":True});assert q.next() is None
