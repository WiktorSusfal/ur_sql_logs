import socket

from uuid import uuid4
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

from threading import Thread, Lock
from time import time, sleep

from lib.models.data_structures.ds_robot_connection_data import DsRobotConnectionData

from lib.helpers.hp_message_parser import HpMessageParser
from lib.helpers.hp_vm_utils import HpVmUtils
from lib.helpers.constants.hp_backend_names import *
from lib.helpers.constants.hp_indicators import *

MdRobotConnBase = declarative_base()
CONNECTION_ERRORS_THRESHOLD = 3


class MdRobotConnection(MdRobotConnBase):

    object_quantity: int = 0

    __tablename__ = ROBOT_INFO_TABLE_NAME

    id = Column(String, primary_key=True)
    name = Column(String)
    ip_address = Column(String)
    port = Column(Integer)
    read_frequency = Column(Float)

    def __init__(self, id: str = None, connection_data: DsRobotConnectionData = None):
        MdRobotConnection.object_quantity += 1

        self._data_lock = Lock()
        self._connection_thread = Thread()
        
        self.id = id or str(uuid4())
        self.update_data(connection_data or DsRobotConnectionData())

        self._connection_status = HEALTH_LOST
        self._connection_status_callbacks = list()

        self._disconnect_flag: bool = False
    
    @HpVmUtils.run_in_thread
    def update_data(self, data: DsRobotConnectionData):
        with self._data_lock:
            self.name = data.name or self._get_default_name()
            self.ip_address = data.ip_address or DEFAULT_IP
            self.port = data.port or DEFAULT_PORT
            self.read_frequency = data.read_freq or DEFAULT_READ_FREQ

    def _get_default_name(self) -> str:
        return '_'.join([DEFAULT_NAME, str(MdRobotConnection.object_quantity)])

    def produce_data_struct(self) -> DsRobotConnectionData:
        return DsRobotConnectionData(self.name, self.ip_address, self.port, self.read_frequency)

    def subscribe_connection_status(self, func):
        if func not in self._connection_status_callbacks:
            self._connection_status_callbacks.append(func)

    def unsubscribe_connection_status(self, func):
        if func in self._connection_status_callbacks:
            self._connection_status_callbacks.remove(func)

    @HpVmUtils.run_in_thread
    def _trigger_connection_status(self, status: int):
        for func in self._connection_status_callbacks:
            func(status)

    @HpVmUtils.run_in_thread
    def connect(self):
        if not self._connection_thread.is_alive():
            with self._data_lock:
                ip, port, freq = self.ip_address, self.port, self.read_frequency
            
            self._connection_thread = Thread(target=self._handle_robot_connection, args=(ip, port, freq))
            self._connection_thread.start()

    @HpVmUtils.run_in_thread
    def disconnect(self):
        with self._data_lock:
            if self._connection_thread.is_alive():
                self._disconnect_flag = True

    def _get_disconnect_flag(self) -> bool:
        with self._data_lock:
            return self._disconnect_flag

    def _handle_robot_connection(self, ip: str, port: int, freq: float):
        robot_connection = self._get_robot_connection(ip, port)
        print(ip, port, freq)
        print(type(robot_connection))
        if not robot_connection:
            return
        
        conn_err_cnt = 0
        while True:
            data, conn_err_cnt = self._get_robot_messages(robot_connection, conn_err_cnt)

            if data:
                HpMessageParser.put_in_queue(data, self.id)

            start_time = time()
            while time() - start_time < freq:
                if conn_err_cnt > CONNECTION_ERRORS_THRESHOLD or self._get_disconnect_flag():
                    self._connection_status = HEALTH_LOST
                    self._trigger_connection_status(HEALTH_LOST)
                    
                    with self._data_lock:
                        self._disconnect_flag = False
                    
                    return
                
                sleep(0.2)

    def _get_robot_connection(self, ip: str, port: str) -> socket.socket:
        robot_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try: 
            robot_connection.connect((ip, port))
            self._connection_status = HEALTH_OK
            self._trigger_connection_status(HEALTH_OK)

        except Exception as e:
            return None
        
        return robot_connection
    
    def _get_robot_messages(self, robot_connection: socket.socket, err_cnt: int) -> tuple[bytes, int]:
        try:
            data = robot_connection.recv(4096)
            return data, err_cnt
        except:
            return None, err_cnt + 1

    
if __name__ == '__main__':
    def connection_indicator(status: int):
        if status == HEALTH_OK:
            print('\nrobot connected\n')
        else:
            print('\nrobot disconnected\n')
    
    rcd = DsRobotConnectionData('name', '127.0.0.1', 30001, 1)
    m = MdRobotConnection('my_robot_id', rcd)
    m.subscribe_connection_status(connection_indicator)
    m.connect()
    sleep(5)
    m.disconnect()
    sleep(4)