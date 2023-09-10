import PyQt5.QtWidgets as qtw

from lib.views.ur_selection_list import URSelectionList
from lib.views.ur_item_details import URItemDetails

from lib.views.components.base_view import URLoggerBaseView
from lib.helpers.gui_tem_names import *

from lib.view_models.application_home import ApplicationHome

class URHomeView(URLoggerBaseView):

    def __init__(self, model: ApplicationHome,  parent=None):
        super(URHomeView, self).__init__(parent=parent)
        self.setObjectName(APPLICATION_HOME_VIEW_NAME)

        self._main_layout = qtw.QGridLayout()
        self.setLayout(self._main_layout)

        self._main_layout.addWidget(URSelectionList(model, parent=self), 0, 0)
        self._main_layout.addWidget(URItemDetails(model, parent=self), 0, 1)
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
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(URHomeView())