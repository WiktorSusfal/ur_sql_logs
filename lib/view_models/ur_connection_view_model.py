from PyQt5.QtCore import QObject, pyqtSignal

from lib.models.ur_connection import URConnection
from lib.models.data_structures.ur_connection_data import URConnectionData


class URConnectionVModel(QObject):

    connection_status_changed = pyqtSignal(bool)
    message_counter_changed = pyqtSignal(int)

    def __init__(self, ur_connection: URConnection = None):
        super(URConnectionVModel, self).__init__()
        self._ur_connection = ur_connection or URConnection()

    def check_connection(self):
        pass

    def update_data(self, data: URConnectionData):
        self._ur_connection._update_data(data.name, data.ip_address, data.port, data.read_freq)