from PyQt5.QtCore import QObject, pyqtSignal

from lib.view_models.vm_4a_robot_connection import VmRobotConnection

from lib.models.md_robot_connection import MdRobotConnection
from lib.models.factories.fmd_robot_connection import FmdRobotConnection

from lib.helpers.utils.hp_vm_utils import HpVmUtils

MAX_CONN_VM_CREATE_ATTEMPTS = 1000


class FvmRobotConnection(QObject):

    connection_created = pyqtSignal(VmRobotConnection)
    connection_removed = pyqtSignal(VmRobotConnection)

    def __init__(self):
        super(FvmRobotConnection, self).__init__()
        self._ur_connections_list: list[VmRobotConnection] = list()

        self._md_factory = FmdRobotConnection()
        self._md_factory.robot_models_get.connect(self._merge_robot_models_data)

    def get_connection_view_model(self, model_id: str) -> VmRobotConnection:
        return next((c for c in self._ur_connections_list if c.robot_id == model_id), None)
    
    def remove_connection_view_model(self, connection: VmRobotConnection):
        self._ur_connections_list.remove(connection)
        self.connection_removed.emit(connection)
    
    def create_connection_view_model(self, model_id: str = None) -> VmRobotConnection:
        conn_vm, is_created = self._create_or_get_conn_vm(model_id)
        if is_created:
            self._append_conn_vm(conn_vm)
        return conn_vm
    
    def _create_or_get_conn_vm(self, model_id: str = None) -> tuple[VmRobotConnection, bool]:
        conn_vm = self.get_connection_view_model(model_id)
        if conn_vm is not None:
            return conn_vm, False
        
        conn_vm = self._create_conn_vm(model_id)
        return conn_vm, True
            
    def _create_conn_vm(self, model_id: str = None) -> VmRobotConnection:
        _iter = -1

        while True:
            _iter += 1
            if _iter >= MAX_CONN_VM_CREATE_ATTEMPTS:
                raise Exception('Cannot create valid VmRobotConnection object')
            
            connection = VmRobotConnection(self._md_factory, model_id)
            if model_id or \
                connection.robot_id not in [c.robot_id for c in self._ur_connections_list]:
                return connection

    @HpVmUtils.run_in_thread
    def _merge_robot_models_data(self, model_list: list[MdRobotConnection]):
        if len(model_list) == 0:
            return
    
        for model in model_list:
            model_data = model.produce_data_struct()
            
            connection_view_model, is_created = self._create_or_get_conn_vm(model.id)
            connection_view_model.check_model_in_db()

            if is_created:
                self._append_conn_vm(connection_view_model)

    def _append_conn_vm(self, vm: VmRobotConnection):
        self._ur_connections_list.append(vm)
        self.connection_created.emit(vm)