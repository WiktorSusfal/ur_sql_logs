from threading import Thread, Lock, Event
from collections.abc import Callable
from time import time, sleep

from lib.helpers.hp_vm_utils import HpVmUtils
from lib.helpers.constants.hp_indicators import *

DEFAULT_MAIN_TASK_INTERVAL = 15.0
DEFAULT_HEALTH_CHECKER = lambda : True
DEFAULT_METHOD = lambda : None


class HpLoopedTaskManager:

    def __init__(self, 
                main_task: Callable[..., bool]
                ,main_args: tuple = tuple()
                ,main_kwargs: dict = dict()
                ,main_interval: float = None
                ,max_task_errors: int = None
                ,health_check: Callable[..., bool] = None
                ,health_args: tuple = tuple()
                ,health_kwargs: dict = dict()
                ,health_interval: float = None
                ,max_health_errors: int = None):
                
        self._main_task = main_task
        self._main_args = main_args         
        self._main_kwargs = main_kwargs     
        self._main_interval = main_interval or DEFAULT_MAIN_TASK_INTERVAL
        self._max_task_errors = max_task_errors
        
        self._health_check = health_check           or DEFAULT_HEALTH_CHECKER
        self._health_args = health_args             
        self._health_kwargs = health_kwargs         
        self._health_interval = health_interval
        self._max_health_errors = max_health_errors

        self._health_ok: bool = False
        self._task_ok: bool = False
        self._abort_flag: bool = False

        self._data_lock: Lock = Lock()
        self._init_health_check = Event()
        self._health_check_thread: Thread = Thread()
        self._main_task_thread: Thread = Thread()
        
        self._health_check_finished: bool = True
        self._main_task_finished: bool = True 

        self._health_status_callbacks: list[Callable[[int], None]] = list()
        self._task_status_callbacks: list[Callable[[int], None]] = list()
        self._process_status_callbacks: list[Callable[[int], None]] = list()

    def set_arguments(self
                      , main_args: tuple = None
                      , main_kwargs: dict = None
                      , health_args: tuple = None
                      , health_kwargs: dict = None
                      , main_interval: float = None
                      , health_interval: float = None):
        
        if not self._main_task_finished or not self._health_check_finished:
            raise Exception(f'Cannot set arguments to {self.__class__.__name__} when process running!')
        
        if main_args is not None: 
            self._main_args = main_args
        if main_kwargs is not None:
            self._main_kwargs = main_kwargs
        if health_args is not None:
            self._health_args = health_args
        if health_kwargs is not None:
            self._health_kwargs = health_kwargs
        if main_interval is not None:
            self._main_interval = main_interval
        if health_interval is not None:
            self._health_interval = health_interval
    
    def subscribe_to_health_status(self, func: Callable[[int], None]):
        if func not in self._health_status_callbacks:
            self._health_status_callbacks.append(func)

    def subscribe_to_task_status(self, func: Callable[[int], None]):
        if func not in self._task_status_callbacks:
            self._task_status_callbacks.append(func)

    def unsubscribe_task_status(self, func: Callable[[int], None]):
        if func in self._task_status_callbacks:
            self._task_status_callbacks.remove(func)

    def subscribe_to_process_status(self, func: Callable[[int], None]):
        if func not in self._process_status_callbacks:
            self._process_status_callbacks.append(func)

    def _trigger_health_callbacks(self, status: int): 
        for func in self._health_status_callbacks:
            func(status)

    def _trigger_task_callbacks(self, status: int):
        for func in self._task_status_callbacks:
            func(status)

    def _trigger_process_status_callbacks(self, status: int):
        for func in self._process_status_callbacks:
            func(status)

    @HpVmUtils.run_in_thread
    def start_process(self):
        with self._data_lock:
            if self._main_task_finished and self._health_check_finished:
                self._start_worker_threads()

    @HpVmUtils.run_in_thread
    def abort_process(self):
        with self._data_lock:
            if not self._main_task_finished and not self._health_check_finished:
                self._abort_flag = True

    @HpVmUtils.run_in_thread
    def _start_worker_threads(self):
        self._trigger_process_status_callbacks(THREADS_RUNNING)

        self._health_check_thread = Thread(target=self._handle_health_check)
        self._health_check_thread.start()

        self._main_task_thread = Thread(target=self._handle_main_task)
        self._main_task_thread.start()

    def _set_health_status(self, status: bool):
        with self._data_lock:
            if self._health_ok != status:
                self._trigger_health_callbacks(HEALTH_OK if status else HEALTH_HAS_ERRORS)
            self._health_ok = status

    def _set_task_status(self, status: bool):
        with self._data_lock:
            if self._task_ok != status:
                self._trigger_task_callbacks(HEALTH_OK if status else HEALTH_HAS_ERRORS)
            self._task_ok = status

    def _get_health_status(self) -> bool:
        with self._data_lock:
            return self._health_ok

    def _get_abort_flag(self) -> bool:
        with self._data_lock:
            return self._abort_flag

    def _handle_health_check(self):
        with self._data_lock:
            self._health_check_finished = False

        health_errors, iter = 0, 0
        while True:
            health = self._health_check(*self._health_args, **self._health_kwargs)
            self._set_health_status(health)
            
            if iter == 0:
                self._init_health_check.set()
            
            health_errors = self._get_err_cnt(health_errors, health)

            start_time = time()
            while self._health_interval is None or \
                    time() - start_time < self._health_interval:
                
                if (self._max_health_errors is not None and health_errors > self._max_health_errors) \
                    or self._get_abort_flag():
                    self._exit_health_check(abort_flag=True, health_status=False)
                    return self._clear_abort_flag()
                
                if self._health_interval is None:
                    self._exit_health_check(abort_flag=not health, health_status=health)
                    return self._clear_abort_flag()
                
                sleep(0.2)
            iter += 1

    def _handle_main_task(self):
        with self._data_lock:
            self._main_task_finished = False

        self._init_health_check.wait()
        task_errors = 0
        while True: 
            if self._get_health_status():
                status = self._main_task(*self._main_args, **self._main_kwargs)
                self._set_task_status(status)

                task_errors = self._get_err_cnt(task_errors, status)

            start_time = time()
            while time() - start_time < self._main_interval:
                if (self._max_task_errors is not None and task_errors > self._max_task_errors) \
                    or self._get_abort_flag():
                    with self._data_lock:
                        self._main_task_finished = True
                        self._abort_flag = True
                        self._task_ok = False
                    return self._clear_abort_flag()
            
                sleep(0.2)

    def _get_err_cnt(self, errors: int, status: bool) -> int:
        if status:
            return 0
        return errors + 1
    
    def _exit_health_check(self, abort_flag: bool, health_status: bool):
        with self._data_lock:
            self._health_check_finished = True
            self._abort_flag = abort_flag
            self._health_ok = health_status

    @HpVmUtils.run_in_thread
    def _clear_abort_flag(self):
        with self._data_lock:
            if self._main_task_finished and self._health_check_finished:
                self._abort_flag = False
        
                if self._health_ok:
                    self._trigger_health_callbacks(HEALTH_LOST)
                if self._task_ok:
                    self._trigger_task_callbacks(HEALTH_LOST)
                self._trigger_process_status_callbacks(THREADS_FINISHED)