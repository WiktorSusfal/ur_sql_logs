import PyQt5.QtWidgets as qtw

from lib.views.components.base_view import BaseView
from lib.views.vw_4b_db_connection_config import VwDBConnectionConfig
from lib.views.vw_4a_app_home import VwAppHome

from lib.helpers.hp_view_models_manager import HpViewModelsManager
from lib.helpers.hp_gui_tem_names import *


class VwMainContent(BaseView):

    def __init__(self, parent=None):
        super(VwMainContent, self).__init__(parent=parent)
        self.setObjectName(CUSTOM_VIEW_WIDGET_NAME)
        self._model = HpViewModelsManager.main_view_model

        self._home_widget = VwAppHome(parent=self)
        self._connection_config = VwDBConnectionConfig(parent=self)

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
    from lib.helpers.hp_visual_view_test_template import visual_test_preview
    visual_test_preview(VwMainContent())