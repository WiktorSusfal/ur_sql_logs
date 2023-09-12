from PyQt5.QtCore import QObject, pyqtSignal

from lib.view_models.vm_4_robot_connection import VmRobotConnection
from lib.models.data_structures.ds_robot_connection_data import DsRobotConnectionData
from lib.helpers.hp_vm_utils import HpVmUtils


class VmRobotDetails(QObject):

    name_changed = pyqtSignal(str)
    ip_changed = pyqtSignal(str)
    port_changed = pyqtSignal(int)
    read_freq_changed = pyqtSignal(int)

    def __init__(self):
        super(VmRobotDetails, self).__init__()

        self._name: str = str()
        self._ip_address: str = str()
        self._port: int = str()
        self._read_frequency: float = float()

        self._vm_robot_connection = VmRobotConnection()

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    @HpVmUtils.observable_property('name', 'name_changed')
    def name(self, name: str):
        self._name = name

    @property
    def ip_address(self) -> str:
        return self._ip_address
    
    @ip_address.setter
    @HpVmUtils.observable_property('ip_address', 'ip_changed')
    def ip_address(self, ip: str):
        self._ip_address = ip

    @property
    def port(self) -> int:
        return self._port
    
    @port.setter
    @HpVmUtils.observable_property('port', 'port_changed')
    def port(self, port: int):
        self._port = port

    @property
    def read_frequency(self) -> float:
        return self._read_frequency
    
    @ip_address.setter
    @HpVmUtils.observable_property('read_frequency', 'read_freq_changed')
    def read_frequency(self, frequency: float):
        self._read_frequency = frequency

    def set_robot_connection_vmodel(self, vm_conn: VmRobotConnection):
        self._vm_robot_connection = vm_conn
        conn_data = vm_conn.ur_connection.produce_data_struct()
        
        self.name = conn_data.name
        self.ip_address = conn_data.ip_address
        self.port = conn_data.port
        self.read_frequency = conn_data.read_freq

if __name__ == '__main__':

    vmd = VmRobotDetails()
    def print_name(n):
        print('Emited: ', n)
    
    vmd.name_changed.connect(print_name)
    vmd.name = 'abc'
    vmd.name = 'abc'
    vmd.name = 'def'
    vmd.name = 'ijk'