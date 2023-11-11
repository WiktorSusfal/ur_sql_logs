"""Contains class which represents robot connection - business model. 
This class is responsible for continuous message reading from robot."""

import socket
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Boolean

from uuid import uuid4
from collections.abc import Callable
from datetime import datetime

from lib.models.data_structures.ds_robot_connection_data import DsRobotConnectionData
from lib.models.components.common import Base

from lib.helpers.messages.hp_message_parser import HpMessageParser
from lib.helpers.utils.looped_tasks.hp_looped_task_manager import HpLoopedTaskManager
from lib.helpers.utils.looped_tasks.hp_looped_task import HpLoopedTask
from lib.helpers.constants.hp_backend_names import *
from lib.helpers.constants.hp_indicators import *

CONNECTION_ERRORS_THRESHOLD = 3
CONNECTION_TIMEOUT = None


class MdRobotConnection(Base):
    """Class which represents robot connection - business model. 
    This class is responsible for continuous message reading from robot."""

    object_quantity: int = 0

    __tablename__   = ROBOT_INFO_TABLE_NAME
    __table_args__  = {'schema': SCHEMA_NAME}

    id              = Column(String, primary_key=True)
    name            = Column(String)
    ip_address      = Column(String)
    port            = Column(Integer)
    read_frequency  = Column(Float)
    is_deleted      = Column(Boolean, default=False)

    comm_msg    = relationship('MDCommMessage'      , backref='robot')
    key_msg     = relationship('MDKeyMessage'       , backref='robot')
    run_exp_msg = relationship('MDRunExpMessage'    , backref='robot')
    safety_msg  = relationship('MDSafetyMessage'    , backref='robot')
    ver_msg     = relationship('MDVersionMessage'   , backref='robot')

    def __init__(self, id: str = None, connection_data: DsRobotConnectionData = None):
        MdRobotConnection.object_quantity += 1

        self._check_health_task_name = 'check_health'
        self._read_data_task_name = 'read_data'
        self._ltm = self._get_task_manager()
        self.subscribe_connection_status(self._dispose_connection)

        self.id = id or str(uuid4())
        self.update_data(connection_data or DsRobotConnectionData())

        self._robot_connection = self._get_robot_connection()

    def update_data(self, data: DsRobotConnectionData):
        self.name = data.name or self._get_default_name()
        self.ip_address = data.ip_address or DEFAULT_IP
        self.port = data.port or DEFAULT_PORT
        self.read_frequency = data.read_freq or DEFAULT_READ_FREQ
        self.is_deleted = data.is_deleted

        self._ltm.set_task_interval(self._read_data_task_name, self.read_frequency)

    def _get_task_manager(self) -> HpLoopedTaskManager:
        health_task = HpLoopedTask(name=self._check_health_task_name, function=self._check_robot_connection, interval=None)
        reading_task = HpLoopedTask(name=self._read_data_task_name
                                    , function=self._get_robot_msg_buffer
                                    , interval=self.read_frequency
                                    , max_errors=CONNECTION_ERRORS_THRESHOLD)

        ltm = HpLoopedTaskManager()
        ltm.register_task(health_task)
        ltm.register_task(reading_task)
        
        ltm.set_task_execution_dependency(self._check_health_task_name, self._read_data_task_name)
        ltm.set_task_status_dependency(self._check_health_task_name, self._read_data_task_name)

        return ltm
        
    def _get_default_name(self) -> str:
        return '_'.join([DEFAULT_NAME, str(MdRobotConnection.object_quantity)])

    def produce_data_struct(self) -> DsRobotConnectionData:
        return DsRobotConnectionData(self.name, self.ip_address, self.port, self.read_frequency, self.is_deleted)

    def subscribe_connection_status(self, func: Callable[[int], None]):
        self._ltm.subscribe_to_process_status(self._read_data_task_name, func)

    def unsubscribe_connection_status(self, func: Callable[[int], None]):
        self._ltm.unsubscribe_process_status(self._read_data_task_name, func)

    def connect(self):
        self._ltm.start_process()

    def disconnect(self):
        self._ltm.abort_process()

    def _dispose_connection(self, status: int):
        if status == THREADS_FINISHED:
            self._robot_connection.close()
            self._robot_connection.detach()

    def _get_robot_connection(self) -> socket.socket:
        robot_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        robot_connection.settimeout(CONNECTION_TIMEOUT)
        return robot_connection

    def _check_robot_connection(self) -> bool:
        try: 
            self._robot_connection = self._get_robot_connection()
            self._robot_connection.connect((self.ip_address, self.port))
            return True
        except Exception as e:
            print(e)
            return False
    
    def _get_robot_msg_buffer(self) -> bool:
        try:
            buffer = self._robot_connection.recv(4096)
            if buffer:
                HpMessageParser.put_in_queue(buffer, self.id, datetime.now())
            return True
        except:
            return False
        
    def __eq__(self, obj):
        if not isinstance(obj, MdRobotConnection):
            return False
        
        return self.id == obj.id and \
                self.name == obj.name and \
                self.ip_address == obj.ip_address and \
                self.port == obj.port and \
                self.read_frequency == obj.read_frequency and \
                self.is_deleted == obj.is_deleted   

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\n\tid={self.id}\n\tname={self.name}\n\tip_address={self.ip_address}"\
                f"\n\tport={self.port}\n\tread_frequency={self.read_frequency}\n\tis_deleted={self.is_deleted}\n)"