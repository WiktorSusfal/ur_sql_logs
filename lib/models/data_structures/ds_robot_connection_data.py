"""Contains data class which encapsulate bunch of data defining robot connection model."""

from dataclasses import dataclass

@dataclass
class DsRobotConnectionData:
    """Data class which encapsulate bunch of data defining robot connection model."""
    name: str = None
    ip_address: str = None
    port: int = None
    read_freq: float = None
    is_deleted: bool = False

    def compare_name(self, name) -> bool:
        return self.name == str(name)
    
    def compare_ip_address(self, ip_address) -> bool:
        return self.ip_address == ip_address
    
    def compare_port(self, port) -> bool:
        try:
            port = int(port)
            return self.port == port
        except:
            return False
        
    def compare_read_freq(self, read_freq) -> bool:
        try:
            read_freq = float(read_freq)
            return self.read_freq == read_freq
        except:
            return False