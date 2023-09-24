from dataclasses import dataclass

@dataclass
class DsRobotRawMessage:
    message: bytes = None
    type: int = None
    robot_id: str = None