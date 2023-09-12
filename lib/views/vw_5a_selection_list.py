import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import BaseView
from lib.views.components.list_widget import URListWidget
from lib.views.vw_6_list_item import VwListItem

from lib.helpers.hp_view_models_manager import HpViewModelsManager, VmRobotConnection
from lib.helpers.hp_gui_tem_names import *


class VwSelectionList(BaseView):

    def __init__(self, parent=None):
        super(VwSelectionList, self).__init__(parent=parent)
        self.setObjectName(UR_SELECTION_LIST_VIEW_NAME)
        self._model = HpViewModelsManager.app_home_view_model
        
        self._selection_list = URListWidget()
        self._add_button = self._produce_button(button_label="+", button_name=LIST_ACTION_BUTTON_NAME)
        self._remove_button = self._produce_button(button_label="-", button_name=LIST_ACTION_BUTTON_NAME)

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self._add_button, alignment=qtc.Qt.AlignLeft)
        button_layout.addWidget(self._remove_button, alignment=qtc.Qt.AlignLeft)
        
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._selection_list, stretch=0)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        self._add_button.clicked.connect(self._model.add_connection)

    def _set_value_subscriptions(self):
        pass

    def _init_actions(self):
        pass

    def add_item(self, connection_item: VmRobotConnection):
        item_widget = VwListItem(connection_item)

        list_item = qtw.QListWidgetItem(self._selection_list)
        list_item.setSizeHint(item_widget.sizeHint())
        self._selection_list.addItem(list_item)
        self._selection_list.setItemWidget(list_item, item_widget)


if __name__ == '__main__':
    from lib.helpers.hp_visual_view_test_template import visual_test_preview
    visual_test_preview(VwSelectionList())