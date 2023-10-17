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

    @property
    def all_tasks_finished(self) -> bool:
        return self._data_manager.all_task_finished()

    def register_task(self, task: HpLoopedTask):
        name = task.get_name()
        
        if name in self._tasks:
            raise Exception('Cannot register two tasks with the same name!')

        task.set_data_manager(self._data_manager)
        self._tasks[name] = task

    def set_task_status_dependency(self, master_task_name: str, child_task_name: str):
        self._tasks[child_task_name].set_dependency_task(master_task_name)

    def set_task_execution_dependency(self, master_task_name: str, child_task_name: str):
        self._tasks[child_task_name].set_waitfor_task(master_task_name)

    @HpVmUtils.run_in_thread
    def start_process(self):
        if self.all_tasks_finished:
            self._start_worker_threads()

    @HpVmUtils.run_in_thread
    def abort_process(self):
        if not self.all_tasks_finished:
            self._data_manager.set_abort_flag(True)   

    def _start_worker_threads(self):
        for task in self._tasks.values():
            task_thread = Thread(target=task.handle_task)
            task_thread.start()    
    
    def subscribe_to_health_status(self, task_name: str, func: Callable[[int], None]):
        self._data_manager.subscribe_task_info(task_name, HEALTH_CALLBACKS, func)

    def unsubscribe_health_status(self, task_name: str, func: Callable[[int], None]):
        self._data_manager.unsubscribe_task_info(task_name, HEALTH_CALLBACKS, func)

    def subscribe_to_process_status(self, task_name: str, func: Callable[[int], None]):
        self._data_manager.subscribe_task_info(task_name, RUNNING_CALLBACKS, func)

    def unsubscribe_process_status(self, task_name: str, func: Callable[[int], None]):
        self._data_manager.unsubscribe_task_info(task_name, RUNNING_CALLBACKS, func)