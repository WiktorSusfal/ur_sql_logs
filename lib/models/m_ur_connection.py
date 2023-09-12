from uuid import uuid4

from lib.models.data_structures.ur_connection_data import URConnectionData

DEFAULT_NAME = "ur_connection"
DEFAULT_IP = '0.0.0.0'
DEFAULT_PORT = 0
DEFAULT_READ_FREQ = 0


class MURConnection:

    object_quantity: int = 0

    def __init__(self, id: str = None, connection_data: URConnectionData = None):
        self.object_quantity += 1
        
        self._id = id or uuid4()
        self._name, self._ip_address = str(), str()
        self._port, self._read_freq = 0, 0
        self._update_data(connection_data or URConnectionData())

    @property
    def id(self) -> str:
        return self._id
    
    def _update_data(self, data: URConnectionData):
        self._name = data.name or self._get_default_name()
        self._ip_address = data.ip_address or DEFAULT_IP
        self._port = data.port or DEFAULT_PORT
        self._read_freq = data.read_freq or DEFAULT_READ_FREQ

    def _get_default_name(self) -> str:
        return '_'.join([DEFAULT_NAME, str(self.object_quantity)])
    
    def _check_connection(self) -> bool:
        pass

    def produce_data_struct(self) -> URConnectionData:
        return URConnectionData(self._name, self._ip_address, self._port, self._read_freq)
