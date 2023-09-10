from dataclasses import dataclass

@dataclass
class URConnectionData:
    name: str
    ip_address: str
    port: int
    read_freq: int