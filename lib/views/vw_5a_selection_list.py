import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import USLBaseView
from lib.views.components.list_widget import USLQListWidget
from lib.views.vw_6a_list_item import VwListItem

from lib.helpers.resources.hp_view_models_manager import HpViewModelsManager, VmRobotConnection
from lib.helpers.constants.hp_gui_tem_names import *


class VwSelectionList(USLBaseView):

    def __init__(self, parent=None):
        super(VwSelectionList, self).__init__(parent=parent)
        self.setObjectName(UR_SELECTION_LIST_VIEW_NAME)
        self._model = HpViewModelsManager.app_home_view_model
        
        self._selection_list = USLQListWidget()
        self._add_button = self._produce_button(button_label="+", button_name=LIST_ACTION_BUTTON_NAME)
        self._delete_button = self._produce_button(button_label="-", button_name=LIST_ACTION_BUTTON_NAME)

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self._add_button, alignment=qtc.Qt.AlignLeft)
        button_layout.addWidget(self._delete_button, alignment=qtc.Qt.AlignLeft)
        
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._selection_list, stretch=0)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        self._add_button.clicked.connect(self._model.add_connection)
        self._delete_button.clicked.connect(self._send_deletion_order)

    def _set_value_subscriptions(self):
        self._model.connection_added.connect(self._add_item)
        self._model.connection_deleted.connect(self._delete_item)

        self._selection_list.currentItemChanged.connect(self._send_item_changed_info)

    def _init_actions(self):
        pass

    def _send_deletion_order(self):
        current_item = self._selection_list.currentItem()
        current_item_view: VwListItem = self._selection_list.itemWidget(current_item)
        if current_item_view:
            current_item_vmodel: VmRobotConnection = current_item_view.model
            self._model.delete_connection(current_item_vmodel)

    def _add_item(self, connection_item: VmRobotConnection):
        item_widget = VwListItem(connection_item, self._selection_list)

        list_item = qtw.QListWidgetItem(self._selection_list)
        list_item.setSizeHint(item_widget.sizeHint())
        
        self._selection_list.addItem(list_item)
        self._selection_list.setItemWidget(list_item, item_widget)
        self._selection_list.setCurrentItem(list_item)

    def _delete_item(self, connection_item: VmRobotConnection):
        current_row = self._selection_list.currentRow()

        item_widget = self._selection_list.takeItem(current_row)
        del item_widget

    def _send_item_changed_info(self, item: qtw.QListWidgetItem):
        item_widget = None
        item_vmodel = None
        if item:
            item_widget: VwListItem = self._selection_list.itemWidget(item)
        if item_widget:
            item_vmodel: VmRobotConnection = item_widget.model
        
        self._model.change_current_connection(item_vmodel)