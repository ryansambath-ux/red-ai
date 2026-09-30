import hashlib
import hmac
import os
import time

MAX_CLOCK_SKEW_SECONDS = 60

def _secret():
    return os.getenv("RED_DEVICE_SECRET", "").encode("utf-8")

def sign(timestamp: str, body: bytes) -> str:
    secret = _secret()
    if not secret:
        raise RuntimeError("RED_DEVICE_SECRET is not configured")
    return hmac.new(secret, timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()

def verify(timestamp: str, body: bytes, signature: str) -> bool:
    secret = _secret()
    if not secret:
        return False
    try:
        if abs(time.time() - int(timestamp)) > MAX_CLOCK_SKEW_SECONDS:
            return False
    except ValueError:
        return False
    expected = hmac.new(secret, timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
