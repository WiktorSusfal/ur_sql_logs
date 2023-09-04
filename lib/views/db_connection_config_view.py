import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from lib.view_models.db_connection_config import DBConnectionConfig

from lib.helpers.gui_tem_names import *
from lib.views.components.base_view import URLoggerBaseView


class CustomItemDelegate(qtw.QStyledItemDelegate):
    def sizeHint(self, option, index):
        return qtc.QSize(option.rect.height(), 30)


class DBConnectionConfigView(URLoggerBaseView):

    def __init__(self, model: DBConnectionConfig):
        super(DBConnectionConfigView, self).__init__()
        self.setObjectName(DB_CONNECTION_VIEW_NAME)
        self._model = model

        self.list_label = qtw.QLabel("Database connection: ")
        self.list_label.setObjectName(FORM_LABEL_NAME)
        self.db_conn_list = qtw.QComboBox()
        self.db_conn_list.setItemDelegate(CustomItemDelegate())
        self.db_conn_list.setFont(qtg.QFont("Roboto", 10))

        self.password_label = qtw.QLabel("Database password: ")
        self.password_label.setObjectName(FORM_LABEL_NAME)
        self.db_password_input = qtw.QLineEdit()
        self.db_password_input.setEchoMode(qtw.QLineEdit.Password)

        self.db_connect_btn = self._produce_button(button_label='Connect', button_name=ACTION_BUTTON_NAME)

        conn_list_layout = qtw.QHBoxLayout()
        conn_list_layout.addWidget(self.list_label, stretch = 0, alignment= qtc.Qt.AlignLeft)
        conn_list_layout.addWidget(self.db_conn_list, stretch = 1, alignment = qtc.Qt.AlignLeft)

        password_layout = qtw.QHBoxLayout()
        password_layout.addWidget(self.password_label, stretch = 0, alignment= qtc.Qt.AlignLeft)
        password_layout.addWidget(self.db_password_input)

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(conn_list_layout)
        main_layout.addLayout(password_layout)
        main_layout.addWidget(self.db_connect_btn, stretch = 0, alignment = qtc.Qt.AlignLeft)
        main_layout.addStretch()

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