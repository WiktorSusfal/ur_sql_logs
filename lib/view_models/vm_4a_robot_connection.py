from PyQt5.QtCore import QObject, pyqtSignal

from lib.models.factories.fmd_robot_connection import FmdRobotConnection
from lib.models.data_structures.ds_robot_connection_data import DsRobotConnectionData

from lib.helpers.messages.hp_message_storage import HpMessageStorage
from lib.helpers.constants.hp_indicators import *


class VmRobotConnection(QObject):

    connection_name_changed = pyqtSignal(str)
    connection_status_changed = pyqtSignal(bool)
    message_counter_changed = pyqtSignal(int)
    db_saved_status_changed = pyqtSignal(int)
    
    def __init__(self, model_factory: FmdRobotConnection, model_id: str = None):
        super(VmRobotConnection, self).__init__()
        self._robot_conn_factory = model_factory
        self._robot_connection = self._robot_conn_factory.create_robot_model(model_id)
        self.subscribe_to_model()

        self.connected: bool = False
        self.db_saved_status: int = 0

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
        self._robot_conn_factory.save_robot_model(self._robot_connection)

    def _connection_status_changed(self, status: int):
        self.connected = False if status == THREADS_FINISHED else True
        self.connection_status_changed.emit(self.connected)

    def mark_as_deleted(self):
        self._robot_conn_factory.delete_robot_model(self._robot_connection)
        
    def _message_counter_changed(self, counter_val: int, **kwargs):
        self.message_counter_changed.emit(counter_val)

    def check_model_in_db(self):
        self.db_saved_status = self._compare_model_with_db()
        self.db_saved_status_changed.emit(self.db_saved_status)
    
    def _compare_model_with_db(self) -> int:
        model_not_exists = 0
        model_saved = 1
        model_has_changes = 2

        robot_model = self._robot_conn_factory.get_robot_model_by_id(self.robot_id)

        if not robot_model:
            return model_not_exists

        if self._robot_connection != robot_model:
            return model_has_changes
        
        return model_saved