from collections.abc import Callable
from threading import Lock

from lib.models.log_messages.md_base_message import MDBaseMessage

MAX_MSG_LIST_SIZE = 25

class HpMessageStorage:

    _messages: dict[str, list[MDBaseMessage] ] = dict()
    _save_staged: list[MDBaseMessage] = dict()

    _message_counter: dict[str, int] = dict()
    _message_counter_callbacks: dict[str, list[Callable[[int], None]] ] = dict()

    _data_lock = Lock()

    @classmethod
    def get_save_staged(cls) -> list[MDBaseMessage]:
        with cls._data_lock:
            result = cls._save_staged.copy()
            cls._save_staged.clear()
        
        return result
    
    @classmethod
    def clear_storage(cls):
        with cls._data_lock:
            cls._messages.clear()

    @classmethod
    def put_in_storage(cls, message: MDBaseMessage, robot_id: str):
        with cls._data_lock:
            cls._save_staged.append(message)
            cls._add_to_storage(message, robot_id)
            cls._message_counter[robot_id] = len(cls._messages[robot_id])

        cls._trigger_message_counter(robot_id)

    @classmethod
    def _add_to_storage(cls, message: MDBaseMessage, robot_id: str):
        if robot_id not in cls._messages:
            cls._messages[robot_id] = list()
        
        if len(cls._messages[robot_id]) >= MAX_MSG_LIST_SIZE:
            cls._messages[robot_id].pop(0)
        
        cls._messages[robot_id].append(message)

    @classmethod
    def subscribe_message_counter(cls, id: str, func: Callable[[int], None]):
        if not id in cls._message_counter_callbacks:
            cls._message_counter_callbacks[id] = [func,]
        else:
            cls._message_counter_callbacks[id].append(func)

    @classmethod
    def unsubscribe_message_counter(cls, id: str, func: Callable[[int], None]):
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