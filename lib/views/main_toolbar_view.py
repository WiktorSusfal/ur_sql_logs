import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

from lib.view_models.main_view_model import URMainViewModel

from lib.views.components.base_view import URLoggerBaseView
from lib.helpers.gui_tem_names import *

class MainToolbarView(URLoggerBaseView):

    def __init__(self, model: URMainViewModel):
        super(MainToolbarView, self).__init__()
        self.setObjectName(MAIN_TOOLBAR_VIEW_WIDGET_NAME)

        self._model = model
       
        self._home_btn = self._produce_icon_button(r'home/home128.png', TOOLBAR_BUTTON_NAME, 50)
        self._settings_btn = self._produce_icon_button(r'gears2/settings_64.png', TOOLBAR_BUTTON_NAME, 50)
        self._help_btn = self._produce_icon_button(r'help/question64.png', TOOLBAR_BUTTON_NAME, 50)

        self._main_layout = qtw.QHBoxLayout()
        self._main_layout.setObjectName('my')
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
    model = URMainViewModel()
    visual_test_preview(MainToolbarView(model))