from app.attention import AttentionEngine

def test_attention_levels():
    engine = AttentionEngine()
    assert engine.classify(2, 2) == "remember"
    assert engine.classify(6, 6) == "summary"
    assert engine.classify(8, 8) == "notify"
    assert engine.classify(10, 10) == "urgent"
