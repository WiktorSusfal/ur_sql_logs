import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.ur_list_widget import URListWidget
from lib.views.ur_list_item import URListItem
from lib.views.components.base_view import URLoggerBaseView
from lib.helpers.gui_tem_names import *


class URSelectionList(URLoggerBaseView):

    def __init__(self):
        super(URSelectionList, self).__init__()
        self.setObjectName(UR_SELECTION_LIST_VIEW_NAME)

        self._selection_list = URListWidget()
        self._add_button = self._produce_button(button_label="+", button_name=LIST_ACTION_BUTTON_NAME)
        self._remove_button = self._produce_button(button_label="-", button_name=LIST_ACTION_BUTTON_NAME)

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self._add_button, alignment=qtc.Qt.AlignLeft)
        button_layout.addWidget(self._remove_button, alignment=qtc.Qt.AlignLeft)
        
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._selection_list, stretch=0)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass

    def _set_value_subscriptions(self):
        pass

    def _init_actions(self):
        pass

    def add_item(self, id: str, title: str):
        item_widget = URListItem(id, title)

        list_item = qtw.QListWidgetItem(self._selection_list)
        list_item.setSizeHint(item_widget.sizeHint())
        self._selection_list.addItem(list_item)
        self._selection_list.setItemWidget(list_item, item_widget)


if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(URSelectionList())