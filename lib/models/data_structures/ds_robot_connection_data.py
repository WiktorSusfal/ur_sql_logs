from dataclasses import dataclass

@dataclass
class DsRobotConnectionData:
    name: str = None
    ip_address: str = None
    port: int = None
    read_freq: int = None