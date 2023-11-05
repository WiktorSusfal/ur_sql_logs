"""Contains data class which encapsulate one single raw robot message (bytes), its type, robot id, and capture date time."""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class DsRobotRawMessage:
    """Data class which encapsulate one single raw robot message (bytes), its type, robot id, and capture date time."""
    message: bytes = None
    type: int = None
    robot_id: str = None
    capture_dt: datetime = None