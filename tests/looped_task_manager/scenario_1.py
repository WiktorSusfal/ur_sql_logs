from time import sleep

from tests.looped_task_manager.base import *


if __name__ == '__main__':

    class TestClass:

        def __init__(self):
            self.t1_cnt = 0
            self.t2_cnt = 0
            self.t3_cnt = 0

        def task_1_func(self) -> bool:
            print('\nDoing task 1')
            self.t1_cnt += 1
            return True
        
        def task_2_func(self) -> bool: 
            print('\nDoing task 2')
            self.t2_cnt += 1
            return True
        
        def task_3_func(self) -> bool:
            print('\nDoing task 3')
            self.t3_cnt += 1
            return self.t3_cnt < 5
        
    tc = TestClass()
    
    task_1 = HpLoopedTask(TASK_1_NAME, tc.task_1_func, interval=None)
    task_2 = HpLoopedTask(TASK_2_NAME, tc.task_2_func, interval=5)
    task_3 = HpLoopedTask(TASK_3_NAME, tc.task_3_func, interval=1, max_errors=4)

    ltm = HpLoopedTaskManager()
    register_tasks(ltm, task_1, task_2, task_3)
    set_task_dependencies(ltm)

    ltm.start_process()
    sleep(12)

    print('All tasks finished: ', ltm._data_manager.all_task_finished())
    print('Abort flag: ', ltm._data_manager.get_abort_flag())