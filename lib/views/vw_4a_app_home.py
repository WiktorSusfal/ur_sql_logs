import PyQt5.QtWidgets as qtw

from lib.views.components.base_view import USLBaseView
from lib.views.vw_5a_selection_list import VwSelectionList
from lib.views.vw_5b_item_details import VwItemDetails

from lib.helpers.constants.hp_gui_tem_names import *


class VwAppHome(USLBaseView):

    def __init__(self, parent=None):
        super(VwAppHome, self).__init__(parent=parent)
        self.setObjectName(APPLICATION_HOME_VIEW_NAME)

        self._main_layout = qtw.QGridLayout()
        self.setLayout(self._main_layout)

        self._main_layout.addWidget(VwSelectionList(parent=self), 0, 0)
        self._main_layout.addWidget(VwItemDetails(parent=self), 0, 1)
        self._style_grid_layout()

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass
    
    def _init_actions(self):
        pass
    
    def _set_value_subscriptions(self):
        pass

    def _style_grid_layout(self):
        self._main_layout.setColumnStretch(0, 0)
        self._main_layout.setColumnStretch(1, 1)
        self._main_layout.setColumnMinimumWidth(0, 270)

if __name__ == '__main__':
    from lib.helpers.utils.hp_visual_view_test_template import visual_test_preview
    visual_test_preview(VwAppHome())