from enum import Enum

class Risk(str, Enum):
    ROUTINE = "routine"
    CONSEQUENTIAL = "consequential"
    CRITICAL = "critical"

class PermissionPolicy:
    """Central safety boundary for Red tools."""
    def requires_confirmation(self, risk: Risk) -> bool:
        return risk in {Risk.CONSEQUENTIAL, Risk.CRITICAL}
