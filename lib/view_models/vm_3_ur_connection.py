from PyQt5.QtCore import QObject, pyqtSignal

from lib.models.m_ur_connection import MURConnection
from lib.models.data_structures.ur_connection_data import URConnectionData


class VMURConnection(QObject):

    ur_connection_changed = pyqtSignal(URConnectionData)
    connection_status_changed = pyqtSignal(bool)
    message_counter_changed = pyqtSignal(int)

    def __init__(self):
        super(VMURConnection, self).__init__()
        self._ur_connection = MURConnection()
        self._connection_status: bool = False
        self._message_counter: int = 0 

    @property
    def connection_data(self):
        return self._ur_connection.produce_data_struct()
        
    @property
    def ur_connection(self) -> MURConnection:
        return self._ur_connection
    
    @ur_connection.setter
    def ur_connection(self, ur_connection: MURConnection):
        self._ur_connection = ur_connection
        self.ur_connection_changed.emit(self.connection_data)

    @property
    def connection_status(self) -> bool:
        return self._connection_status
    
    @connection_status.setter
    def connection_status(self, status: bool):
        self._connection_status = status
        self.connection_status_changed.emit(self._connection_status)

    @property
    def message_counter(self) -> bool:
        return self._message_counter
    
    @message_counter.setter
    def message_counter(self, counter: int):
        self._message_counter = counter
        self.message_counter_changed.emit(self._message_counter)

    def update_data(self, data: URConnectionData):
        self._ur_connection._update_data(data)