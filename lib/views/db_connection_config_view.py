import PyQt5.QtWidgets as qtw

from lib.helpers.gui_tem_names import *
from lib.views.base_view import URLoggerBaseView
from lib.view_models.db_connection_config import DBConnectionConfig

class DBConnectionConfigView(URLoggerBaseView):

    def __init__(self, model: DBConnectionConfig):
        super(DBConnectionConfigView, self).__init__()

        self.setWindowTitle("Choose database connection")

        self._model = model

        self.list_label = qtw.QLabel("Choose database connection: ")
        self.list_label.setObjectName(FORM_LABEL_NAME)
        self.db_conn_list = qtw.QComboBox()

        self.password_label = qtw.QLabel("Enter database password: ")
        self.password_label.setObjectName(FORM_LABEL_NAME)
        self.db_password_input = qtw.QLineEdit()
        self.db_password_input.setEchoMode(qtw.QLineEdit.Password)

        self.db_connect_btn = qtw.QPushButton(text='Connect')

        conn_list_layout = qtw.QHBoxLayout()
        conn_list_layout.addWidget(self.list_label)
        conn_list_layout.addWidget(self.db_conn_list)
        password_layout = qtw.QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.db_password_input)

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(conn_list_layout)
        main_layout.addLayout(password_layout)
        main_layout.addWidget(self.db_connect_btn)

        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _set_value_subscriptions(self):
        self._model.db_names_changed.connect(self._db_connection_names_changed)

    def _bind_buttons_to_commands(self):
        pass

    def _init_actions(self):
        self._model.get_connection_names()

    def _db_connection_names_changed(self):
        names = self._model.db_connection_names
        self.db_conn_list.addItems(names)


if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    conn_config_model = DBConnectionConfig()
    visual_test_preview(DBConnectionConfigView(conn_config_model))