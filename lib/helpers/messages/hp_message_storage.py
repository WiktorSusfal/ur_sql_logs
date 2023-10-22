from collections.abc import Callable
from threading import Lock

from lib.models.log_messages.md_base_message import MDBaseMessage

MAX_MSG_LIST_SIZE = 250

class HpMessageStorage:

    _messages: dict[str, list[MDBaseMessage] ] = dict()
    _save_staged: list[MDBaseMessage] = list()
    _message_counter: dict[str, int] = dict()

    _message_counter_callbacks: dict[str, list[Callable[[int, dict], None]] ] = dict()

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
    def get_robot_messages(cls, robot_id: str, msg_cnt: int = None) -> list[MDBaseMessage]:
        if robot_id not in cls._messages:
            return list()
        
        with cls._data_lock:   
            if msg_cnt:
                return cls._messages[robot_id][-msg_cnt:]
            return cls._messages[robot_id]

    @classmethod
    def put_in_storage(cls, message: MDBaseMessage, robot_id: str):
        with cls._data_lock:
            cls._save_staged.append(message)
            cls._add_to_storage(message, robot_id)
            cls._message_counter[robot_id] = len(cls._messages[robot_id])

        counter_kwargs = {'last_message': message,}
        cls._trigger_message_counter(robot_id, counter_kwargs)

    @classmethod
    def _add_to_storage(cls, message: MDBaseMessage, robot_id: str):
        if robot_id not in cls._messages:
            cls._messages[robot_id] = list()
        
        if len(cls._messages[robot_id]) >= MAX_MSG_LIST_SIZE:
            cls._messages[robot_id].pop(0)
        
        cls._messages[robot_id].append(message)

    @classmethod
    def subscribe_message_counter(cls, id: str, func: Callable[[int, dict], None]):
        with cls._data_lock:
            if not id in cls._message_counter_callbacks:
                cls._message_counter_callbacks[id] = [func,]
            else:
                cls._message_counter_callbacks[id].append(func)

    @classmethod
    def unsubscribe_message_counter(cls, id: str, func: Callable[[int, dict], None]):
        with cls._data_lock:
            if id not in cls._message_counter_callbacks:
                return
            if func in cls._message_counter_callbacks[id]:
                cls._message_counter_callbacks[id].remove(func)
            if len(cls._message_counter_callbacks[id]) == 0:
                del cls._message_counter_callbacks[id]

    @classmethod
    def _trigger_message_counter(cls, id: str, counter_kwargs: dict):
        with cls._data_lock:
            value = cls._message_counter[id]
            for func in cls._message_counter_callbacks[id]:
                func(value, **counter_kwargs)