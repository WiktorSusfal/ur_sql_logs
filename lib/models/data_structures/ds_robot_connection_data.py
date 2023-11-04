from dataclasses import dataclass

@dataclass
class DsRobotConnectionData:
    name: str = None
    ip_address: str = None
    port: int = None
    read_freq: float = None
    is_deleted: bool = False