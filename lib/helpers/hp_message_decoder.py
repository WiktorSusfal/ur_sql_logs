from queue import Queue
from threading import Lock

from lib.models.data_structures.ds_robot_raw_message import DsRobotRawMessage

from lib.helpers.hp_looped_task_manager import HpLoopedTaskManager

class HpMessageDecoder:

    _data_lock: Lock = Lock()
    _input_messages: Queue[DsRobotRawMessage] = Queue(1000)

    _ltm: HpLoopedTaskManager = None

    _message_counter: dict[str, int] = dict()
    _message_counter_callbacks: dict[str, list] = dict()

    @classmethod
    def put_in_queue(cls, raw_message: bytes, message_type: int, robot_id):
        if not cls._ltm:
            cls._ltm = cls._get_task_manager()
            cls._ltm.start_process()

        with cls._data_lock:
            cls._input_messages.put_nowait(DsRobotRawMessage(raw_message, message_type, robot_id))

    @classmethod
    def subscribe_message_counter(cls, id: str, func):
        if not id in cls._message_counter_callbacks:
            cls._message_counter_callbacks[id] = [func,]
        else:
            cls._message_counter_callbacks[id].append(func)

    @classmethod
    def unsubscribe_message_counter(cls, id: str, func):
        if id not in cls._message_counter_callbacks:
            return
        if func in cls._message_counter_callbacks[id]:
            cls._message_counter_callbacks[id].remove(func)
        if len(cls._message_counter_callbacks[id]) == 0:
            del cls._message_counter_callbacks[id]

    @classmethod
    def _trigger_message_counter(cls, id: str):
        value = cls._message_counter[id]
        for func in cls._message_counter_callbacks[id]:
            func(value)

    @classmethod
    def _get_task_manager(cls) -> HpLoopedTaskManager:
        return HpLoopedTaskManager()