from lib.helpers.utils.looped_tasks.hp_looped_task_manager import HpLoopedTaskManager
from lib.helpers.utils.looped_tasks.hp_looped_task import HpLoopedTask

from lib.helpers.constants.hp_indicators import *

status_map = {HEALTH_OK: 'HEALTH_OK', HEALTH_HAS_ERRORS: 'HAS_ERRORS', HEALTH_LOST: 'HEALTH_LOST'}

TASK_1_NAME = 'task_1'
TASK_2_NAME = 'task_2'
TASK_3_NAME = 'task_3'

def task_1_running_callback(running: int):
    print('\nTASK_1 ' + ('RUNNING' if running == THREADS_RUNNING else 'FINISHED'))

def task_2_running_callback(running: int):
    print('\nTASK_2 ' + ('RUNNING' if running == THREADS_RUNNING else 'FINISHED'))

def task_3_running_callback(running: int):
    print('\nTASK_3 ' + ('RUNNING' if running == THREADS_RUNNING else 'FINISHED'))

def task_1_health_callback(status: int):
    print('\nTASK_1 ' + status_map.get(status, 'UNKNOWN STATUS'))

def task_2_health_callback(status: int):
    print('\nTASK_2 ' + status_map.get(status, 'UNKNOWN STATUS'))

def task_3_health_callback(status: int):
    print('\nTASK_3 ' + status_map.get(status, 'UNKNOWN STATUS'))

def register_tasks(ltm: HpLoopedTaskManager, *tasks):
    for task in tasks:
        ltm.register_task(task)

def set_task_dependencies(ltm: HpLoopedTaskManager):
    ltm.set_task_execution_dependency(TASK_1_NAME, TASK_2_NAME)
    ltm.set_task_execution_dependency(TASK_2_NAME, TASK_3_NAME)
    ltm.set_task_status_dependency(TASK_2_NAME, TASK_3_NAME)

    ltm.subscribe_to_health_status(TASK_1_NAME, task_1_health_callback)
    ltm.subscribe_to_health_status(TASK_2_NAME, task_2_health_callback)
    ltm.subscribe_to_health_status(TASK_3_NAME, task_3_health_callback)
    ltm.subscribe_to_process_status(TASK_1_NAME, task_1_running_callback)
    ltm.subscribe_to_process_status(TASK_2_NAME, task_2_running_callback)
    ltm.subscribe_to_process_status(TASK_3_NAME, task_3_running_callback)