from threading import Thread
from collections.abc import Callable

from lib.helpers.utils.looped_tasks.hp_looped_task import HpLoopedTask
from lib.helpers.utils.looped_tasks.hp_task_data_manager import HpTaskDataManager, HEALTH_CALLBACKS, RUNNING_CALLBACKS
from lib.helpers.utils.hp_vm_utils import HpVmUtils
from lib.helpers.constants.hp_indicators import *


class HpLoopedTaskManager:

    def __init__(self):
        self._data_manager = HpTaskDataManager()
        self._tasks: dict[str, HpLoopedTask] = dict()

    def register_task(self
                        ,name: str
                        ,function: Callable[..., bool]
                        ,args: tuple = tuple()
                        ,kwargs: dict = dict()
                        ,interval: float = None
                        ,max_errors: int = None):
        
        if name in self._tasks:
            raise Exception('Cannot register two tasks with the same name!')
        
        task = HpLoopedTask(self._data_manager, name, function, args, kwargs, interval, max_errors)
        self._tasks[name] = task

    def set_task_status_dependency(self, master_task_name: str, child_task_name: str):
        self._tasks[child_task_name].set_dependency_task(master_task_name)

    def set_task_execution_dependency(self, master_task_name: str, child_task_name: str):
        self._tasks[child_task_name].set_waitfor_task(master_task_name)

    @HpVmUtils.run_in_thread
    def start_process(self):
        if self._data_manager.all_task_finished():
            self._start_worker_threads()

    @HpVmUtils.run_in_thread
    def abort_process(self):
        if not self._data_manager.all_task_finished():
            self._data_manager.set_abort_flag(True)   

    def _start_worker_threads(self):
        for task in self._tasks.values():
            task_thread = Thread(target=task.handle_task)
            task_thread.start()    
    
    def subscribe_to_health_status(self, task_name: str, func: Callable[[int], None]):
        self._data_manager.subscribe_task_status(task_name, HEALTH_CALLBACKS, func)

    def unsubscribe_health_status(self, task_name: str, func: Callable[[int], None]):
        self._data_manager.unsubscribe_task_status(task_name, HEALTH_CALLBACKS, func)

    def subscribe_to_process_status(self, task_name: str, func: Callable[[int], None]):
        self._data_manager.subscribe_task_status(task_name, RUNNING_CALLBACKS, func)