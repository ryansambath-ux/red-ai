import time
from app import device_auth

def test_signed_device_message(monkeypatch):
    monkeypatch.setenv("RED_DEVICE_SECRET", "test-secret")
    timestamp = str(int(time.time()))
    body = b'{"name":"notepad"}'
    signature = device_auth.sign(timestamp, body)
    assert device_auth.verify(timestamp, body, signature)

def test_modified_message_fails(monkeypatch):
    monkeypatch.setenv("RED_DEVICE_SECRET", "test-secret")
    timestamp = str(int(time.time()))
    signature = device_auth.sign(timestamp, b"original")
    assert not device_auth.verify(timestamp, b"changed", signature)
