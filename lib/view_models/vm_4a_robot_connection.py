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
    db_saved_status_changed = pyqtSignal(int)
    
    def __init__(self, model_id: str = None):
        super(VmRobotConnection, self).__init__()
        self._robot_connection = MdRobotConnection(model_id)
        self.subscribe_to_model()

        self.connected: bool = False

    @property
    def robot_connection_data(self):
        return self._robot_connection.produce_data_struct()
    
    @property
    def robot_connection_name(self) -> str:
        return self.robot_connection_data.name
    
    @property
    def robot_id(self) -> str:
        return self._robot_connection.id

    def update_data(self, data: DsRobotConnectionData):
        self._robot_connection.update_data(data)
        self.connection_name_changed.emit(data.name)

    def subscribe_to_model(self):
        self._robot_connection.subscribe_connection_status(
            self._connection_status_changed)
        HpMessageStorage.subscribe_message_counter(
            self._robot_connection.id, self._message_counter_changed)
        
    def connect_to_robot(self):
        self._robot_connection.connect()

    def disconnect_from_robot(self):
        self._robot_connection.disconnect()

    def save_robot_model(self):
        HpDBConnectionManager.save_robot_model(self._robot_connection)

    def _connection_status_changed(self, status: int):
        self.connected = False if status == THREADS_FINISHED else True
        self.connection_status_changed.emit(self.connected)

    def mark_as_deleted(self):
        self._robot_connection.is_deleted = True
        self.save_robot_model() 

    def _message_counter_changed(self, counter_val: int, **kwargs):
        self.message_counter_changed.emit(counter_val)

    def check_model_in_db(self):
        status = self._compare_model_with_db()
        self.db_saved_status_changed.emit(status)
    
    def _compare_model_with_db(self) -> int:
        model_not_exists = 0
        model_saved = 1
        model_has_changes = 2

        
        robot_model = HpDBConnectionManager.get_robot_model_by_id(self.robot_id)

        if not robot_model:
            print('comparing - not exists')
            return model_not_exists

        if self._robot_connection != robot_model:
            print('comparing - not the same')
            return model_has_changes
        
        print('comparing - the same')
        return model_saved