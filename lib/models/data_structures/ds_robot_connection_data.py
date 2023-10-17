from dataclasses import dataclass

@dataclass
class DsRobotConnectionData:
    name: str = None
    ip_address: str = None
    port: int = None
    read_freq: int = None


    def __repr__(self):
        return f"{self.__class__.__name__} with params:\n"\
                f"name: {self.name}, ip_address: {self.ip_address}, port: {self.port}, read_freq: {self.read_freq}"