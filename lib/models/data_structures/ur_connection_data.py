from dataclasses import dataclass

@dataclass
class URConnectionData:
    name: str = None
    ip_address: str = None
    port: int = None
    read_freq: int = None