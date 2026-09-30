# Red Windows Agent

This component will run on Ryan's Windows computer and execute authenticated commands from Red Core.

The first version intentionally exposes only allow-listed actions:
- open selected applications
- open HTTP/HTTPS websites
- search Documents and Downloads

It does not provide unrestricted shell access.

## Development test

From the repository root:

```
python
>>> from windows_agent.agent import open_app, find_file
>>> open_app("notepad")
>>> find_file("manual")
```

The next stage adds an authenticated local API, Red Core pairing, voice/wake-word support and Windows startup/background-service packaging.
