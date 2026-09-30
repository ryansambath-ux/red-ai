from app.events import EventStore
def test_events(tmp_path):
 s=EventStore(str(tmp_path/"e.json"));e=s.add("test","hello","notify")
 assert len(s.unread())==1;s.mark_read(e["id"]);assert s.unread()==[]
