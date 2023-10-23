from PyQt5.QtCore import QObject, pyqtSignal

from lib.view_models.vm_3_robot_details import VmRobotDetails
from lib.view_models.vm_4a_robot_connection import VmRobotConnection

from lib.models.md_robot_connection import MdRobotConnection

from lib.helpers.database.hp_db_connection_manager import HpDBConnectionManager
from lib.helpers.utils.hp_vm_utils import HpVmUtils


class VmAppHome(QObject):

    connection_added = pyqtSignal(VmRobotConnection)
    connection_deleted = pyqtSignal(VmRobotConnection)

    def __init__(self):
        super(VmAppHome, self).__init__()
        self._ur_connections_list: list[VmRobotConnection] = list()
        self.robot_details: VmRobotDetails = VmRobotDetails()

        HpDBConnectionManager.subscribe_to_robot_models_get(self._merge_robot_models_data)
        
    def add_connection(self, connection: VmRobotConnection = None):
        if not connection:
            connection = self._create_connection_view_model()

        self._ur_connections_list.append(connection)
        self.connection_added.emit(connection)

    def _create_connection_view_model(self, model_id: str = None) -> VmRobotConnection:
        while True:
            connection = VmRobotConnection(model_id)
            if model_id or \
                connection.robot_id not in [c.robot_id for c in self._ur_connections_list]:
                return connection

    def delete_connection(self, connection: VmRobotConnection):
        connection.mark_as_deleted()
        self._ur_connections_list.remove(connection)
        self.connection_deleted.emit(connection)

    def change_current_connection(self, connection: VmRobotConnection):
        robot_connection = next((c for c in self._ur_connections_list if c == connection), None)
    
        if robot_connection == self.robot_details._vm_robot_connection:
            return
          
        self.robot_details.set_robot_connection_vmodel(robot_connection)

    @HpVmUtils.run_in_thread
    def _merge_robot_models_data(self, model_list: list[MdRobotConnection]):
        if len(model_list) == 0:
            return
        
        present = True
        for model in model_list:
            
            model_data = model.produce_data_struct()
            connection_view_model = next((c for c in self._ur_connections_list if c.robot_id == model.id), None)
            
            if not connection_view_model:
                connection_view_model = self._create_connection_view_model(model.id)
                present = False
        
            connection_view_model.update_data(model_data)

            if not present:
                self.add_connection(connection_view_model)
                present = True

            connection_view_model.check_model_in_db()