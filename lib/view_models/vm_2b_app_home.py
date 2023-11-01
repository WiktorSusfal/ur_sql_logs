from PyQt5.QtCore import QObject, pyqtSignal

from lib.view_models.vm_3_robot_details import VmRobotDetails
from lib.view_models.factories.fvm_robot_connection import FvmRobotConnection, VmRobotConnection


class VmAppHome(QObject):

    connection_added = pyqtSignal(VmRobotConnection)
    connection_deleted = pyqtSignal(VmRobotConnection)

    def __init__(self):
        super(VmAppHome, self).__init__()
        self._vm_factory = FvmRobotConnection()
        self.robot_details: VmRobotDetails = VmRobotDetails()

        self._vm_factory.connection_created.connect(
            self.connection_added.emit)
        self._vm_factory.connection_removed.connect(
            self.connection_deleted.emit)
        
    def add_connection(self):
        self._vm_factory.create_connection_view_model()

    def delete_connection(self, connection: VmRobotConnection):
        connection.mark_as_deleted()
        self._vm_factory.remove_connection_view_model(connection)

    def change_current_connection(self, connection: VmRobotConnection):
        id = connection.robot_id if connection else None
        robot_connection = self._vm_factory.get_connection_view_model(id)
    
        if robot_connection == self.robot_details._vm_robot_connection:
            return
          
        self.robot_details.set_robot_connection_vmodel(robot_connection)