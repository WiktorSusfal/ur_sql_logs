import PyQt5.QtWidgets as qtw

from lib.views.components.base_view import USLBaseView

from lib.helpers.constants.hp_gui_tem_names import *

HELP_TEXT = """
        <h1>UR SQL Logger</h1>
        <p>Application made for saving log messages read from industrial robot to a SQL database.</p>
        <p>The robot model that was used to create the application is Universal Robot UR10 e-Series.<br>
        Software version: 5.13.1.</p>
        <p>SQL database is Postgres in version 15.4.</p>
        """

class VwHelp(USLBaseView):

    def __init__(self, parent=None):
        super(VwHelp, self).__init__(parent=parent)
        self.setObjectName(HELP_VIEW_NAME)

        self._content = qtw.QTextBrowser()
        self._content.setObjectName(HELP_TEXT_WIDGET_NAME)
        self._content.setHtml(HELP_TEXT)

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._content)

        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass
    
    def _init_actions(self):
        pass
    
    def _set_value_subscriptions(self):
        pass