# Voice and alerts

Red 0.6 adds browser speech input/output using the device browser's Web Speech support. This is intentionally separate from the future always-listening Windows wake-word process.

The event inbox stores proactive Red events with four attention levels: remember, summary, notify and urgent.

Production phone push notifications still require Firebase/Android credentials. Until those are configured, the PWA can surface events when opened.

Wake-word listening will be local to the Windows device so continuous microphone audio does not need to be streamed to the cloud.
