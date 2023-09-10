import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.db_connection_config_view import DBConnectionConfigView
from lib.views.application_home_view import URHomeView

from lib.view_models.main_view_model import URMainViewModel

from lib.views.components.base_view import URLoggerBaseView
from lib.helpers.gui_tem_names import *


class MainContentView(URLoggerBaseView):

    def __init__(self, model: URMainViewModel, parent=None):
        super(MainContentView, self).__init__(parent=parent)
        self.setObjectName(CUSTOM_VIEW_WIDGET_NAME)
        self._model = model

        self._home_widget = URHomeView(self._model.app_home_vmodel, parent=self)
        self._connection_config = DBConnectionConfigView(self._model.db_connection_vmodel, parent=self)

        self._widget_manager = qtw.QStackedWidget()
        self._widget_manager.addWidget(self._home_widget)
        self._widget_manager.addWidget(self._connection_config)
        
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._widget_manager, stretch=1)
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass
    
    def _init_actions(self):
        pass
    
    def _set_value_subscriptions(self):
        self._model.content_view_index_changed.connect(self.set_current_widget)
    
    def set_current_widget(self, index: int):
        if index > self._widget_manager.count() - 1:
            return
        self._widget_manager.setCurrentIndex(index)
    
    
if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(MainContentView())