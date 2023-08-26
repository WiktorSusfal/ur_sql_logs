from PyQt5.QtCore import QObject, pyqtSignal

from lib.helpers.connection_config_data import ConnectionConfigData

class DBConnectionConfig(QObject):

    db_names_changed = pyqtSignal()

    def __init__(self):
        super(DBConnectionConfig, self).__init__()
        self._db_connection_names: list[str] = list()
        self._db_password = str()

    @property
    def db_connection_names(self):
        return self._db_connection_names
    
    @db_connection_names.setter
    def db_connection_names(self, connection_names: list[str]):
        self._db_connection_names = connection_names
        self.db_names_changed.emit()

    def get_connection_names(self):
        self.db_connection_names = ConnectionConfigData.get_db_connection_names()

    def connect_to_database(self):
        pass