import socket
from collections.abc import Callable

from uuid import uuid4
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

from lib.models.data_structures.ds_robot_connection_data import DsRobotConnectionData

from lib.helpers.hp_message_parser import HpMessageParser
from lib.helpers.hp_looped_task_manager import HpLoopedTaskManager
from lib.helpers.constants.hp_backend_names import *
from lib.helpers.constants.hp_indicators import *

MdRobotConnBase = declarative_base()
CONNECTION_ERRORS_THRESHOLD = 3
CONNECTION_TIMEOUT = 1.5


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

        self._ltm = HpLoopedTaskManager(
            main_task = self._get_robot_msg_buffer
            ,main_interval = self.read_frequency
            ,max_task_errors = CONNECTION_ERRORS_THRESHOLD
            ,health_check = self._check_robot_connection
            ,health_interval = None #check only once at the beginning
        )
        
        self.id = id or str(uuid4())
        self.update_data(connection_data or DsRobotConnectionData())

        self._robot_connection =self._get_robot_connection()
        
        
    
    def update_data(self, data: DsRobotConnectionData):
        self.name = data.name or self._get_default_name()
        self.ip_address = data.ip_address or DEFAULT_IP
        self.port = data.port or DEFAULT_PORT
        self.read_frequency = data.read_freq or DEFAULT_READ_FREQ

        self._ltm.set_arguments(main_interval=self.read_frequency)

    def _get_default_name(self) -> str:
        return '_'.join([DEFAULT_NAME, str(MdRobotConnection.object_quantity)])

    def produce_data_struct(self) -> DsRobotConnectionData:
        return DsRobotConnectionData(self.name, self.ip_address, self.port, self.read_frequency)

    def subscribe_connection_status(self, func: Callable[[int], None]):
        self._ltm.subscribe_to_task_status(func)

    def unsubscribe_connection_status(self, func: Callable[[int], None]):
        self._ltm.unsubscribe_task_status(func)

    def connect(self):
        self._robot_connection = self._get_robot_connection()
        self._ltm.start_process()

    def disconnect(self):
        self._ltm.abort_process()

    def _get_robot_connection(self) -> socket.socket:
        robot_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        robot_connection.settimeout(CONNECTION_TIMEOUT)
        return robot_connection

    def _check_robot_connection(self) -> bool:
        try: 
            self._robot_connection.connect((self.ip_address, self.port))
            return True
        except Exception as e:
            return False
    
    def _get_robot_msg_buffer(self) -> bool:
        try:
            buffer = self._robot_connection.recv(4096)
            if buffer:
                HpMessageParser.put_in_queue(buffer, self.id)
            return True
        except:
            return False