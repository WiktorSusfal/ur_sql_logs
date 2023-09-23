from PyQt5.QtCore import QObject, pyqtSignal

from lib.helpers.hp_db_connection_manager import HpDBConnectionManager
from lib.helpers.resources.hp_connection_config_data import HpConnectionConfigData
from lib.helpers.hp_vm_utils import HpVmUtils

class VmDBConnectionConfig(QObject):

    db_names_changed = pyqtSignal(list)

    db_connect_status_changed = pyqtSignal(int)
    db_threads_status_changed = pyqtSignal(int)

    def __init__(self):
        super(VmDBConnectionConfig, self).__init__()
        self._db_connection_names: list[str] = list()
        self._current_connection = str()
        self._db_password = str()

        HpDBConnectionManager.subscribe_to_health_status(self.db_connect_status_changed.emit)
        HpDBConnectionManager.subscribe_to_threads_status(self.db_threads_status_changed.emit)
    
    @HpVmUtils.observable_property('_db_connection_names', 'db_names_changed')
    def set_connection_names(self, connection_names: list[str]):
        self._db_connection_names = connection_names

    def set_current_connection(self, connection_name: str):
        self._current_connection = connection_name

    def set_password(self, password: str):
        self._db_password = password

    def get_connection_names(self):
        names = HpConnectionConfigData.get_db_connection_names()
        self.set_connection_names(names)

    def connect_to_database(self):
        c_string = HpConnectionConfigData.get_db_connection_string(self._current_connection
                                                                    , self._db_password)
        HpDBConnectionManager.set_connection_string(c_string)
        HpDBConnectionManager.connect()

    def disconnect_from_database(self):
        HpDBConnectionManager.disconnect()