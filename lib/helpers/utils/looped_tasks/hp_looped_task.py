from threading import Event
from collections.abc import Callable
from time import time, sleep

from lib.helpers.utils.looped_tasks.hp_task_data_manager import HpTaskDataManager

MIN_INTERVAL = 0.1


class HpLoopedTask:

    def __init__(self
                ,name: str
                ,function: Callable[..., bool]
                ,args: tuple = tuple()
                ,kwargs: dict = dict()
                ,interval: float = None
                ,max_errors: int = None ):
    
        self._name = name
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self._interval = interval
        self._max_errors = max_errors

        self._data_manager = None

        self._health_checker_name: str = None
        self._waitfor_name: str = None

    def get_name(self) -> str:
        return self._name
    
    def set_data_manager(self, dm: HpTaskDataManager):
        self._data_manager = dm
        self._data_manager.register_task(self._name)

    def set_interval(self, interval: float):
        self._interval = interval

    def set_dependency_task(self, task_name: str):
        self._health_checker_name = task_name

    def set_waitfor_task(self, task_name: str):
        self._waitfor_name = task_name

    def handle_task(self):
        self._data_manager.set_running_info(self._name, True)
        self._wait_for_dependency()

        errors, iter = 0, -1
        while True:
            if self._check_health():
                iter += 1

                task_status = self._function(*self._args, **self._kwargs)
                self._data_manager.set_succeeded_info(self._name, task_status, force_notification=not bool(iter))

                if iter == 0:
                    self._data_manager.set_executed_once_event(self._name)

                errors = self._get_err_cnt(errors, task_status)
 
                if self._interval is None:  
                    self._exit_task(task_status=task_status, abort_flag=not task_status)
                    return
            
            start_time = time()
            while time() - start_time < self._interval:
                
                if (self._max_errors is not None and errors > self._max_errors) \
                        or self._data_manager.get_abort_flag():
                    
                    self._exit_task(task_status=False, abort_flag=True)
                    return
                
                sleep(MIN_INTERVAL)

    def _wait_for_dependency(self):
        if self._waitfor_name:
            executed_event: Event = self._data_manager.get_executed_once_event(self._waitfor_name)
            executed_event.wait()

    def _check_health(self) -> bool:
        if self._health_checker_name:
            return self._data_manager.get_succeeded_info(self._health_checker_name)
        
        return True

    def _get_err_cnt(self, errors: int, status: bool) -> int:
        if status:
            return 0
        return errors + 1
    
    def _exit_task(self, task_status: bool, abort_flag: bool):
        self._data_manager.set_abort_flag(abort_flag)
        self._data_manager.set_running_info(self._name, False, force_notification=True)
        self._data_manager.set_succeeded_info(self._name, task_status, force_notification=True)