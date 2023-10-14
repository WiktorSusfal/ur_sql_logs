from PyQt5.QtCore import QObject, pyqtSignal

from lib.view_models.vm_3_robot_details import VmRobotDetails
from lib.view_models.vm_4_robot_connection import VmRobotConnection


class VmAppHome(QObject):

    connection_added = pyqtSignal(VmRobotConnection)
    connection_deleted = pyqtSignal(VmRobotConnection)

    def __init__(self):
        super(VmAppHome, self).__init__()
        self._ur_connections_list: list[VmRobotConnection] = list()
        self.robot_details: VmRobotDetails = VmRobotDetails()
        
    def add_connection(self):
        connection = VmRobotConnection()
        self._ur_connections_list.append(connection)
        self.connection_added.emit(connection)

    def delete_connection(self, connection: VmRobotConnection):
        self._ur_connections_list.remove(connection)
        self.connection_deleted.emit(connection)

    def change_current_connection(self, connection: VmRobotConnection):
        robot_connection = next((c for c in self._ur_connections_list if c == connection), None)
    
        if robot_connection == self.robot_details._vm_robot_connection:
            return
        
        self.robot_details.set_robot_connection_vmodel(robot_connection)