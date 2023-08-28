import PyQt5.QtWidgets as qtw

from lib.views.db_connection_config_view import DBConnectionConfigView, DBConnectionConfig

from lib.views.components.base_view import URLoggerBaseView
from lib.helpers.gui_tem_names import *


class MainContentView(URLoggerBaseView):

    def __init__(self):
        super(MainContentView, self).__init__()

        self._home_widget = qtw.QLabel("Placeholder")
        self._connection_config = DBConnectionConfigView(DBConnectionConfig())

        self._widget_manager = qtw.QStackedWidget()
        self._widget_manager.addWidget(self._home_widget)
        self._widget_manager.addWidget(self._connection_config)
        
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._widget_manager)
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        return super()._bind_buttons_to_commands()
    
    def _init_actions(self):
        return super()._init_actions()
    
    def _set_value_subscriptions(self):
        return super()._set_value_subscriptions()
    
    def set_current_widget(self, index: int):
        if index > self._widget_manager.count() - 1:
            return
        self._widget_manager.setCurrentIndex(index)
    
if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(MainContentView())