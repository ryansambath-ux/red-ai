class AttentionEngine:
    """Scores events before Red decides whether to interrupt the user."""

    LEVELS = {
        "remember": 4,
        "summary": 6,
        "notify": 8,
        "urgent": 10,
    }

    def classify(self, relevance: int, urgency: int) -> str:
        score = max(0, min(10, round((relevance + urgency) / 2)))
        if score >= self.LEVELS["urgent"]:
            return "urgent"
        if score >= self.LEVELS["notify"]:
            return "notify"
        if score >= self.LEVELS["summary"]:
            return "summary"
        return "remember"
