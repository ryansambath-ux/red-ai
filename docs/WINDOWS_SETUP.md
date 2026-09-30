# Windows Agent setup

After Red Core has a public HTTPS Cloud Run URL:

1. Install Python 3.12 on the Windows PC.
2. Clone this repository.
3. Install requirements.
4. Set `RED_CORE_URL` to the Cloud Run URL.
5. Set `RED_AGENT_TOKEN` to the same strong secret configured on Red Core.
6. Run `python -m windows_agent.client`.

The agent makes outbound HTTPS requests to Red Core. No router port-forwarding is required. Only allow-listed actions are executed.

A Windows startup/service installer will be added after live pairing is tested.
