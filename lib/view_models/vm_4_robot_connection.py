from PyQt5.QtCore import QObject, pyqtSignal

from lib.models.md_robot_connection import MdRobotConnection
from lib.models.data_structures.ds_robot_connection_data import DsRobotConnectionData

from lib.helpers.messages.hp_message_storage import HpMessageStorage
from lib.helpers.database.hp_db_connection_manager import HpDBConnectionManager
from lib.helpers.constants.hp_indicators import *


class VmRobotConnection(QObject):

    connection_name_changed = pyqtSignal(str)
    connection_status_changed = pyqtSignal(bool)
    message_counter_changed = pyqtSignal(int)
    
    def __init__(self):
        super(VmRobotConnection, self).__init__()
        self._robot_connection = MdRobotConnection()
        self.subscribe_to_model()

        self.connected: bool = False

    @property
    def robot_connection_data(self):
        return self._robot_connection.produce_data_struct()
    
    @property
    def robot_connection_name(self) -> str:
        return self.robot_connection_data.name

    def update_data(self, data: DsRobotConnectionData):
        self._robot_connection.update_data(data)
        self.connection_name_changed.emit(data.name)

    def subscribe_to_model(self):
        self._robot_connection.subscribe_connection_status(
            self._connection_status_changed)
        HpMessageStorage.subscribe_message_counter(
            self._robot_connection.id, self.message_counter_changed.emit)
        
    def connect_to_robot(self):
        self._robot_connection.connect()

    def disconnect_from_robot(self):
        self._robot_connection.disconnect()

    def save_robot_model(self):
        HpDBConnectionManager.save_robot_model(self._robot_connection)

    def _connection_status_changed(self, status: int):
        self.connected = False if status == THREADS_FINISHED else True
        self.connection_status_changed.emit(self.connected)