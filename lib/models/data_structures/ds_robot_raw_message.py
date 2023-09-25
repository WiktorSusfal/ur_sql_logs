from dataclasses import dataclass
from datetime import datetime

@dataclass
class DsRobotRawMessage:
    message: bytes = None
    type: int = None
    robot_id: str = None
    capture_dt: datetime = None