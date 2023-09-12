from PyQt5.QtCore import QObject, pyqtSignal

from lib.view_models.vm_3_ur_connection import VMURConnection

from lib.models.m_ur_connection import MURConnection


class VMAppHome(QObject):

    connection_added = pyqtSignal(VMURConnection)
    connection_deleted = pyqtSignal(VMURConnection)
    current_connection_changed = pyqtSignal(VMURConnection)

    def __init__(self):
        super(VMAppHome, self).__init__()
        self._ur_connections_list: list[VMURConnection] = list()
        self._current_connection = VMURConnection()

    def add_connection(self):
        connection = VMURConnection()
        self._ur_connections_list.append(connection)
        self.connection_added.emit(connection)

    def delete_connection(self, connection: VMURConnection):
        self._ur_connections_list.remove(connection)
        self.connection_deleted.emit(connection)

    def change_current_connection(self, connection: VMURConnection):
        self.current_connection_changed.emit(connection)