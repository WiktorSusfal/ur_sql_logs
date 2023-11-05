"""Contains class which decodes bytes of particular robot's message into given set of values. 
Creates relevant message object and passes it to the message storage in cache."""

from queue import Queue
from threading import Lock
from datetime import datetime

from lib.models.data_structures.ds_robot_raw_message import DsRobotRawMessage
from lib.models.log_messages.md_base_message import MDBaseMessage
from lib.models.log_messages.md_comm_message import MDCommMessage
from lib.models.log_messages.md_key_message import MDKeyMessage
from lib.models.log_messages.md_run_exp_message import MDRunExpMessage
from lib.models.log_messages.md_safety_message import MDSafetyMessage
from lib.models.log_messages.md_version_message import MDVersionMessage

from lib.helpers.messages.hp_message_storage import HpMessageStorage
from lib.helpers.utils.looped_tasks.hp_looped_task_manager import HpLoopedTaskManager
from lib.helpers.utils.looped_tasks.hp_looped_task import HpLoopedTask

DECODING_INTERVAL = 0.1
MSG_MODEL_TYPE_MAP: dict[int, type] = {
                                        3: MDVersionMessage,
                                        7: MDKeyMessage,
                                        5: MDSafetyMessage,
                                        6: MDCommMessage,
                                        10: MDRunExpMessage
                                    }

class HpMessageDecoder:
    """Class which decodes bytes of particular robot's message into given set of values. 
    Creates relevant message object and passes it to the message storage in cache."""

    _data_lock: Lock = Lock()
    _input_messages: Queue[DsRobotRawMessage] = Queue(1000)

    _ltm: HpLoopedTaskManager = None

    @classmethod
    def put_in_queue(cls, raw_message: bytes, message_type: int, robot_id, capture_dt: datetime):
        if not cls._ltm:
            cls._ltm = cls._get_task_manager()
        
        if cls._ltm.all_tasks_finished:
            cls._ltm.start_process()

        with cls._data_lock:
            cls._input_messages.put_nowait(DsRobotRawMessage(raw_message, message_type, robot_id, capture_dt))

    @classmethod
    def _decode_messages(cls) -> bool:
        raw_msg = cls._get_next_msg()
        if raw_msg is None:
            return False
        
        msg_class = cls._get_msg_class(raw_msg.type)
        if  not msg_class:
            return False
        
        msg_object = cls._get_msg_object(msg_class, raw_msg.message, raw_msg.robot_id, raw_msg.capture_dt)
        msg_object.decode_message()
        HpMessageStorage.put_in_storage(msg_object, raw_msg.robot_id)

        return True
    
    @classmethod
    def _get_msg_class(cls, msg_type: int) -> type:
        return MSG_MODEL_TYPE_MAP.get(msg_type, None)
    
    @staticmethod
    def _get_msg_object(msg_class: type, msg: bytes, robot_id: str, capture_dt: datetime) -> MDBaseMessage:
        return msg_class(msg, robot_id, capture_dt)
    
    @classmethod
    def _get_next_msg(cls) -> DsRobotRawMessage:
        try:
            with cls._data_lock:
                raw_msg = cls._input_messages.get_nowait()
            return raw_msg
        except:
            return None

    @classmethod
    def _get_task_manager(cls) -> HpLoopedTaskManager:
        decode_task = HpLoopedTask(name='decoding_task', function=cls._decode_messages, interval=DECODING_INTERVAL)
        ltm = HpLoopedTaskManager()
        ltm.register_task(decode_task)
        return ltm