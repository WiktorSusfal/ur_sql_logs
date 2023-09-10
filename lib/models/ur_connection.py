from uuid import uuid4

DEFAULT_NAME = "ur_connection"
DEFAULT_IP = '0.0.0.0'
DEFAULT_PORT = 0
DEFAULT_READ_FREQ = 0

class URConnection:

    object_quantity: int = 0

    def __init__(self, id: str = None, name: str = None, ip_address: str = None, port: int = None, read_freq: float = None):
        self.object_quantity += 1
        
        self._id = id or uuid4()
        self._name, self._ip_address = str(), str()
        self._port, self._read_freq = 0, 0
        self._update_data(name, ip_address, port, read_freq)

    def _get_default_name(self) -> str:
        return '_'.join([DEFAULT_NAME, self.object_quantity])
    
    def _update_data(self, name: str, ip_address: str, port: int, read_freq: float):
        self._name = name or self._get_default_name()
        self._ip_address = ip_address or DEFAULT_IP
        self._port = port or DEFAULT_PORT
        self._read_freq = read_freq or DEFAULT_READ_FREQ
    
    def _check_connection(self) -> bool:
        pass
