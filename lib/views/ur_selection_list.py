import PyQt5.QtWidgets as qtw

from lib.views.ur_list_item import URListItem
from lib.views.components.base_view import URLoggerBaseView
from lib.helpers.gui_tem_names import *


class URSelectionList(URLoggerBaseView):

    def __init__(self):
        super(URLoggerBaseView, self).__init__()

        self._selection_list = qtw.QListWidget()

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._selection_list)
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