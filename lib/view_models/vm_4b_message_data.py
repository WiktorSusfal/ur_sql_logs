from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtCore as qtc
from threading import Lock

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.messages.hp_message_storage import HpMessageStorage
from lib.helpers.utils.hp_vm_utils import HpVmUtils
from lib.helpers.utils.looped_tasks.hp_looped_task import HpLoopedTask
from lib.helpers.utils.looped_tasks.hp_looped_task_manager import HpLoopedTaskManager

MAX_ITEMS = 25
REFRESH_DATA_INTERVAL = 0.5


class VmMessageData(QStandardItemModel):

    init_message_added = qtc.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(VmMessageData, self).__init__(parent)

        self._robot_id: str = None
        self._horizontal_labels = ['type', 'timestamp', 'source', 'rmsg_type', 'custom data']
        self.setHorizontalHeaderLabels(self._horizontal_labels)

        self._staged_data_lock = Lock()
        self._control_lock = Lock()

        self._staged_rows = set()
        self._reload_flag = False

        self._ltm = self._set_task_manager()
        self._ltm.start_process()

    def set_robot_id(self, robot_id: str):
        HpMessageStorage.unsubscribe_message_counter(self._robot_id, self._message_arrived)
        HpMessageStorage.subscribe_message_counter(robot_id, self._message_arrived)

        self._robot_id = robot_id
        self._robot_id_changed()
        
    @HpVmUtils.run_in_thread
    def _robot_id_changed(self):
        self._refresh_staged_rows()
        self._set_reload_data_flag(True)
   
    def _refresh_staged_rows(self):
        current_messages = HpMessageStorage.get_robot_messages(self._robot_id, MAX_ITEMS)
        self._append_staged_rows(current_messages, clear_existing=True)

    def _append_staged_rows(self, stg_rows: list[MDBaseMessage], clear_existing: bool = False):
        with self._staged_data_lock:
            if clear_existing:
                self._staged_rows.clear()

            self._staged_rows = self._staged_rows.union(set(stg_rows))
    
    def _append_staged_row(self, staged_row: MDBaseMessage):
        with self._staged_data_lock:
            self._staged_rows.add(staged_row)
    
    def _get_staged_rows(self) -> set[MDBaseMessage]:
        with self._staged_data_lock:
            result = self._staged_rows.copy()
            self._staged_rows.clear()
            return result
        
    def _set_reload_data_flag(self, status: bool):
        with self._control_lock:
            self._reload_flag = status

    def _get_reload_data_flag(self):
        with self._control_lock:
            return self._reload_flag

    @HpVmUtils.run_in_thread
    def _message_arrived(self, overall_count: int, **kwargs):
        last_message: MDBaseMessage = kwargs.get('last_message', None)
        if not last_message:
            return
        
        self._append_staged_row(last_message)

    def _set_task_manager(self) -> HpLoopedTaskManager:
        task = HpLoopedTask('UPDATE_TASK', self._update_data, interval=REFRESH_DATA_INTERVAL)
        ltm = HpLoopedTaskManager()
        ltm.register_task(task)
        return ltm
    
    def _update_data(self):
        reload_flag = self._get_reload_data_flag()
        if reload_flag:
            self._reload_data()
        else:
            self._append_data()

    def _reload_data(self):
        self._set_reload_data_flag(False)
        self.clear()
        self.setHorizontalHeaderLabels(self._horizontal_labels)
        self._append_data()

    def _append_data(self):
        staged_rows = self._get_staged_rows()
        staged_rows = sorted(staged_rows, key=lambda sr: sr.date_time)
        for sr in staged_rows:
            self._append_row(sr)

    def _append_row(self, message: MDBaseMessage):
        next_row = self.rowCount()
        items = self._build_data_row(message)

        for idx, item in enumerate(items):
            if next_row == MAX_ITEMS:
                self.removeRow(0)
                next_row -= 1
            self.setItem(next_row, idx, item)

        if next_row == 0:
            self.init_message_added.emit(True)
  
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