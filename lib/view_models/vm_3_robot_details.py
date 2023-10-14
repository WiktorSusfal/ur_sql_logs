from PyQt5.QtCore import QObject, pyqtSignal

from lib.view_models.vm_4_robot_connection import VmRobotConnection

from lib.models.data_structures.ds_robot_connection_data import DsRobotConnectionData

from lib.helpers.utils.hp_vm_utils import HpVmUtils
from lib.helpers.database.hp_db_connection_manager import HpDBConnectionManager


class VmRobotDetails(QObject):

    name_changed = pyqtSignal(str)
    ip_changed = pyqtSignal(str)
    port_changed = pyqtSignal(str)
    read_freq_changed = pyqtSignal(str)

    db_connect_status_changed = pyqtSignal(int)
    model_empty = pyqtSignal(bool)

    def __init__(self):
        super(VmRobotDetails, self).__init__()

        self._name: str = str()
        self._ip_address: str = str()
        self._port: str = str()
        self._read_frequency: str = str()

        self._vm_robot_connection: VmRobotConnection = None

        HpDBConnectionManager.subscribe_to_health_status(self.db_connect_status_changed.emit)
    
    @HpVmUtils.observable_property('_name', 'name_changed')
    def set_name(self, name: str):
        self._name = name
    
    @HpVmUtils.observable_property('_ip_address', 'ip_changed')
    def set_ip_address(self, ip: str):
        self._ip_address = ip

    @HpVmUtils.observable_property('_port', 'port_changed')
    def set_port(self, port: str):
        self._port = port
    
    @HpVmUtils.observable_property('_read_frequency', 'read_freq_changed')
    def set_read_frequency(self, frequency: str):
        self._read_frequency = frequency

    def set_robot_connection_vmodel(self, vm_conn: VmRobotConnection):
        self._vm_robot_connection = vm_conn
        self.model_empty.emit(vm_conn is None)
        self.update_interface_data()
        
    def update_interface_data(self):
        if self._vm_robot_connection:
            conn_data = self._vm_robot_connection.robot_connection_data
        else:
            conn_data = DsRobotConnectionData()
        
        self.set_name(conn_data.name)
        self.set_ip_address(conn_data.ip_address)
        self.set_port(str(conn_data.port))
        self.set_read_frequency(str(conn_data.read_freq))

    def save_interface_data(self):
        if self._vm_robot_connection:
            data = DsRobotConnectionData(self._name, self._ip_address, int(self._port), float(self._read_frequency))
            self._vm_robot_connection.update_data(data)
            self._save_to_db()

    @HpVmUtils.run_in_thread
    def _save_to_db(self):
        self._vm_robot_connection.save_robot_model()
        
    def robot_connect(self):
        self._vm_robot_connection.connect_to_robot()

    def robot_disconnect(self):
        self._vm_robot_connection.disconnect_from_robot()