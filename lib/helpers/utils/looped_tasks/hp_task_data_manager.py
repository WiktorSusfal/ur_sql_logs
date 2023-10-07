from threading import Lock, Event
from collections.abc import Callable
from dataclasses import dataclass

from lib.helpers.utils.looped_tasks.hp_looped_task_data import HpLoopedTaskData, RUNNING_INFO, SUCCEEDED_INFO
from lib.helpers.constants.hp_indicators import *

RUNNING_CALLBACKS = 0
HEALTH_CALLBACKS = 1


@dataclass
class CallbackCategory:
    task_name: str = None
    info_type: int = None


class HpTaskDataManager:

    def __init__(self):
        self._data_lock = Lock()
        self._data: dict[str, HpLoopedTaskData] = dict()

        self._abort_flag = Event()

        self._callbacks: dict[CallbackCategory, list[Callable[[int, int], None]]] = dict()

    def set_abort_flag(self, flag: bool):
        with self._data_lock:
            if flag:
                self._abort_flag.set()
            else:
                self._abort_flag.clear()

    def get_abort_flag(self) -> bool:
        with self._data_lock:
            return self._abort_flag.is_set()
        
    def all_task_finished(self) -> bool:
        with self._data_lock:
            run_statuses = [td.running for td in self._data.values() if td.running == True]
            return len(run_statuses) == 0

    def register_task(self, name: str):
        with self._data_lock:
            self._data[name] = HpLoopedTaskData()
            # register category for callbacks about this task
            running_category = CallbackCategory(name, RUNNING_CALLBACKS)
            status_category = CallbackCategory(name, HEALTH_CALLBACKS)

            self._callbacks[running_category] = list()
            self._callbacks[status_category] = list()

    def get_executed_once_event(self, task_name: str) -> Event:
        with self._data_lock:
            task_data = self._data.get(task_name, None)
            if not task_data:
                return None
        
            return task_data.executed_once_event
    
    def set_executed_once_event(self, task_name: str):
        with self._data_lock:
            if task_name not in self._data:
                return
        
            self._data[task_name].executed_once_event.set()

    def set_running_info(self, task_name: str, value: bool):
        self._set_info(task_name, value, RUNNING_INFO)
        self._trigger_task_running_callbacks(task_name, value)
        if not value:
            self._clear_abort_flag()

    def get_running_info(self, task_name: str) -> bool:
        return self._get_info(task_name, RUNNING_INFO)

    def set_succeeded_info(self, task_name: str, value: bool):
        self._set_info(task_name, value, SUCCEEDED_INFO)
        self._trigger_task_health_callbacks(task_name, value)

    def get_succeeded_info(self, task_name: str) -> bool:
        return self._get_info(task_name, SUCCEEDED_INFO)
    
    def _set_info(self, task_name: str, value: bool, info_type: int):
        with self._data_lock:
            task_data = self._data.get(task_name, None)
            if not task_data:
                return None
        
            return task_data.set_info(value, info_type)
    
    def _get_info(self, task_name: str, info_type: int) -> bool:
        with self._data_lock:
            task_data = self._data.get(task_name, None)
            if not task_data:
                return None
        
            return task_data.get_info(info_type)
        
    def _clear_abort_flag(self):
        if not self.get_abort_flag():
            return 
            
        if self.all_task_finished():
            self.set_abort_flag(False)

    def subscribe_task_status(self, task_name: str, category: int, func: Callable[[int, int], None]):
        category = CallbackCategory(task_name, category)
        
        if func not in self._callbacks[category]:
            self._callbacks[category].append(func)

    def unsubscribe_task_status(self, task_name: str, category: int, func: Callable[[int, int], None]):
        category = CallbackCategory(task_name, category)
        
        if func in self._callbacks[category]:
            self._callbacks[category].remove(func)

    def _trigger_task_health_callbacks(self, task_name: str, health_status: bool, task_running: bool = None):
        category = CallbackCategory(task_name, HEALTH_CALLBACKS)
        if category in self._callbacks:
            
            if task_running is None:
                task_running = self.get_running_info(task_name)

            report_status = self._get_report_task_status(health_status, task_running)
            
            for func in self._callbacks[category]:
                func(report_status)

    def _trigger_task_running_callbacks(self, task_name: str, task_running: bool):
        category = CallbackCategory(task_name, RUNNING_CALLBACKS)
        if category in self._callbacks:

            report_status = THREADS_RUNNING if task_running else THREADS_FINISHED
            
            for func in self._callbacks[category]:
                func(report_status)

    def _get_report_task_status(self, task_status: bool, task_running: bool):
        if not task_running:
            return HEALTH_LOST
        elif not task_status:
            return HEALTH_HAS_ERRORS
        else:
            return HEALTH_OK