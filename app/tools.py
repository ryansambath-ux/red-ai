class ToolRegistry:
    """Allow-listed tools Red is permitted to use."""

    def __init__(self):
        self.tools = {
            "help": self.help,
            "capabilities": self.help,
        }

    def try_command(self, text: str):
        command = text.strip().lower()
        fn = self.tools.get(command)
        return fn() if fn else None

    def help(self):
        return {
            "reply": (
                "Red 0.1 core is running. Current tools: status and capabilities. "
                "Weather, web research, memory, Windows control and notifications are next."
            ),
            "action": "capabilities",
        }
