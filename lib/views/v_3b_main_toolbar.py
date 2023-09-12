import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.view_models.vm_1_main import VMMain

from lib.views.components.base_view import BaseView
from lib.helpers.gui_tem_names import *

class VMainToolbar(BaseView):

    def __init__(self, model: VMMain, parent=None):
        super(VMainToolbar, self).__init__(parent)
        self.setObjectName(MAIN_TOOLBAR_VIEW_WIDGET_NAME)

        self._model = model
       
        self._home_btn = self._produce_button(r'home/home128.png', 35, TOOLBAR_BUTTON_NAME)
        self._settings_btn = self._produce_button(r'gears2/settings_64.png', 35, TOOLBAR_BUTTON_NAME)
        self._help_btn = self._produce_button(r'help/question64.png', 35, TOOLBAR_BUTTON_NAME)

        self._main_layout = qtw.QHBoxLayout()
        self._main_layout.addWidget(self._home_btn, stretch = 0)
        self._main_layout.addWidget(self._settings_btn, stretch = 0)
        self._main_layout.addWidget(self._help_btn, stretch = 0, alignment = qtc.Qt.AlignRight)

        self.setLayout(self._main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        self._home_btn.clicked.connect(self._model.set_home_view)
        self._settings_btn.clicked.connect(self._model.set_db_connection_view)
        self._help_btn.clicked.connect(self._model.set_help_view)

    def _init_actions(self):
        pass

    def _set_value_subscriptions(self):
        pass
    

if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    model = VMMain()
    visual_test_preview(VMainToolbar(model))