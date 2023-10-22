from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtCore as qtc
from threading import Thread, Lock

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.messages.hp_message_storage import HpMessageStorage
from lib.helpers.utils.hp_vm_utils import HpVmUtils
from lib.helpers.utils.looped_tasks.hp_looped_task import HpLoopedTask
from lib.helpers.utils.looped_tasks.hp_looped_task_manager import HpLoopedTaskManager

MAX_ITEMS = 25
REFRESH_DATA_INTERVAL = 0.1

class VmMessageData(QStandardItemModel):

    def __init__(self, parent=None):
        super(VmMessageData, self).__init__(parent)

        self._robot_id: str = None
        self._horizontal_labels = ['type', 'timestamp', 'source', 'rmsg_type', 'custom data']
        self.setHorizontalHeaderLabels(self._horizontal_labels)

        self._data_lock = Lock()
        self._data_thread_list: list[Thread] = list()

        self._ltm = self._set_task_manager()
        self._ltm.start_process()

    def _set_task_manager(self) -> HpLoopedTaskManager:
        task = HpLoopedTask('UPDATE_TASK', self._manage_update_tasks, interval=REFRESH_DATA_INTERVAL)
        ltm = HpLoopedTaskManager()
        ltm.register_task(task)
        return ltm

    def set_robot_id(self, robot_id: str):
        HpMessageStorage.unsubscribe_message_counter(self._robot_id, self._message_arrived)
        self._robot_id = robot_id
        self._robot_id_changed()
        
    @HpVmUtils.run_in_thread
    def _robot_id_changed(self):
        self._refresh_dataset()
        HpMessageStorage.subscribe_message_counter(self._robot_id, self._message_arrived)

    def _refresh_dataset(self):
        current_messages = HpMessageStorage.get_robot_messages(self._robot_id, MAX_ITEMS)
        thread = Thread(target=self._reload_data, args=(current_messages, ))
        self._schedule_thread(thread, clear_existing=True)

    @HpVmUtils.run_in_thread
    def _message_arrived(self, overall_count: int, **kwargs):
        last_message = kwargs.get('last_message', None)
        if not last_message:
            return
        
        thread = Thread(target=self._append_message, args=(last_message, ))
        self._schedule_thread(thread)
        
    def _append_message(self, message: MDBaseMessage):
        next_row = self.rowCount()
        items = self._build_data_row(message)

        for idx, item in enumerate(items):
            if next_row == MAX_ITEMS:
                self.removeRow(0)
                next_row -= 1
            self.setItem(next_row, idx, item)

    def _reload_data(self, msg_list: list[MDBaseMessage]):
        self.clear()
        self.setHorizontalHeaderLabels(self._horizontal_labels)

        for msg in msg_list:
            self._append_message(msg)
        
    def _build_data_row(self, message: MDBaseMessage) -> list[QStandardItem]:
        m = message
        items: list[QStandardItem] = list()
   
        items.append(self._data_item(m.msg_type))
        items.append(self._data_item(m.date_time))
        items.append(self._data_item(m.source_name))
        items.append(self._data_item(m.robot_message_type))

        custom_data = m._get_custom_data_as_string()
        items.append(self._data_item(custom_data))
        return items
    
    def _data_item(self, value) -> QStandardItem:
        item = QStandardItem(str(value))
        item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        return item
        
    def _schedule_thread(self, thread: Thread, clear_existing: bool = False):
        with self._data_lock:
            if clear_existing:
                self._data_thread_list.clear()
            self._data_thread_list.append(thread)

    def _get_next_thread(self) -> Thread:
        with self._data_lock:
            if len(self._data_thread_list) > 0: 
                return self._data_thread_list.pop(0)
            return None
            
    def _manage_update_tasks(self) -> bool:
        thread = self._get_next_thread()
        
        if thread:
            thread.start()
            thread.join()

        return True