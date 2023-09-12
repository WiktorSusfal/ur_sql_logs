import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from lib.view_models.vm_2a_db_connection_config import VMDBConnectionConfig

from lib.helpers.gui_tem_names import *
from lib.views.components.base_view import BaseView


class CustomItemDelegate(qtw.QStyledItemDelegate):
    def sizeHint(self, option, index):
        return qtc.QSize(option.rect.height(), 30)


class VDBConnectionConfig(BaseView):

    def __init__(self, model: VMDBConnectionConfig, parent=None):
        super(VDBConnectionConfig, self).__init__(parent=parent)
        self.setObjectName(DB_CONNECTION_VIEW_NAME)
        self._model = model

        self._list_label = qtw.QLabel("Database connection: ")
        self._list_label.setObjectName(FORM_LABEL_NAME)
        self._db_conn_list = qtw.QComboBox()
        self._db_conn_list.setItemDelegate(CustomItemDelegate())
        self._db_conn_list.setFont(qtg.QFont("Roboto", 10))

        self._password_label = qtw.QLabel("Database password: ")
        self._password_label.setObjectName(FORM_LABEL_NAME)
        self._db_password_input = qtw.QLineEdit()
        self._db_password_input.setEchoMode(qtw.QLineEdit.Password)

        self._db_connect_btn = self._produce_button(button_label='Connect', button_name=ACTION_BUTTON_NAME)
        self._db_disconnect_btn = self._produce_button(button_label='Disconnect', button_name=ACTION_BUTTON_NAME)

        conn_list_layout = qtw.QHBoxLayout()
        conn_list_layout.addWidget(self._list_label, stretch = 0, alignment= qtc.Qt.AlignLeft)
        conn_list_layout.addWidget(self._db_conn_list, stretch = 1, alignment = qtc.Qt.AlignLeft)

        password_layout = qtw.QHBoxLayout()
        password_layout.addWidget(self._password_label, stretch = 0, alignment= qtc.Qt.AlignLeft)
        password_layout.addWidget(self._db_password_input, stretch = 1, alignment= qtc.Qt.AlignLeft)

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self._db_connect_btn, stretch=0, alignment=qtc.Qt.AlignLeft)
        button_layout.addWidget(self._db_disconnect_btn, stretch=0, alignment=qtc.Qt.AlignLeft)
        button_layout.addStretch()

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(conn_list_layout, stretch=0)
        main_layout.addLayout(password_layout, stretch=0)
        main_layout.addLayout(button_layout, stretch=0)
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
        self._db_conn_list.addItems(names)


if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    conn_config_model = VMDBConnectionConfig()
    visual_test_preview(VDBConnectionConfig(conn_config_model))