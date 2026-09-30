from app.memory import MemoryStore

def test_memory_round_trip(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    store.remember("Verdant is a project", "project")
    assert store.recent(1)[0]["text"] == "Verdant is a project"
