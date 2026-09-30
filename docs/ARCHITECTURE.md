# Red architecture

## Cloud
Red Core is designed for Google Cloud Run. It owns conversation routing, memory coordination, attention decisions and model/tool selection.

## Device
The Windows Agent performs only allow-listed local actions. Its HTTP listener binds to 127.0.0.1 by default, so it is not exposed directly to the internet.

Commands are authenticated with an HMAC device secret and a short timestamp window. A later pairing/tunnel layer will let Cloud Red reach the local agent without opening an inbound router port.

## Reasoning
The reasoning layer is provider-independent through an OpenAI-compatible endpoint. Provider credentials belong in environment variables / cloud secret storage, never Git.

## Action policy
Routine actions may execute automatically. Consequential and critical actions require confirmation before execution.
