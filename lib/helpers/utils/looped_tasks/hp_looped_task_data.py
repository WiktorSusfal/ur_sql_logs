from dataclasses import dataclass
from threading import Event

RUNNING_INFO = 0
SUCCEEDED_INFO = 1

@dataclass
class HpLoopedTaskData:
    succeeded: bool = False
    running: bool = False
    executed_once_event: Event = Event()

    def get_info(self, info_type: int) -> bool:
        if info_type == RUNNING_INFO:
            return self.running
        elif info_type == SUCCEEDED_INFO:
            return self.succeeded
        
    def set_info(self, value: bool, info_type: int):
        if info_type == RUNNING_INFO:
            self.running = value
        elif info_type == SUCCEEDED_INFO:
            self.succeeded = value