import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from lib.views.components.base_view import USLBaseView

from lib.helpers.hp_view_models_manager import HpViewModelsManager
from lib.helpers.constants.hp_gui_tem_names import *
from lib.helpers.constants.hp_indicators import *


class _CustomItemDelegate(qtw.QStyledItemDelegate):
    def sizeHint(self, option, index):
        return qtc.QSize(option.rect.width(), 30)


class VwDBConnectionConfig(USLBaseView):

    def __init__(self, parent=None):
        super(VwDBConnectionConfig, self).__init__(parent=parent)
        self.setObjectName(DB_CONNECTION_VIEW_NAME)
        self._model = HpViewModelsManager.db_config_view_model
        
        self._db_conn_list = qtw.QComboBox()
        self._db_conn_list.setItemDelegate(_CustomItemDelegate())
        self._db_conn_list.setFont(qtg.QFont("Roboto", 10))

        self._db_password_input = self._produce_line_edit(FORM_INPUT_NAME, echo_mode=qtw.QLineEdit.Password)

        main_form = qtw.QFormLayout()
        main_form.addRow(
            self._produce_named_label("Database connection: ", FORM_LABEL_NAME)  
            ,self._db_conn_list)
        main_form.addRow(
            self._produce_named_label("Database password: ", FORM_LABEL_NAME)
            ,self._db_password_input)
        
        self._db_connect_btn = self._produce_button(button_label='Connect', button_name=ACTION_BUTTON_NAME)
        self._db_disconnect_btn = self._produce_button(button_label='Disconnect', button_name=ACTION_BUTTON_NAME)

        self._conn_icon_label = self._produce_icon_label(r'connected/dbcon52.png', 52, 52, label_name=FORM_ICON_LABEL_NAME)
        self._disconn_icon_label = self._produce_icon_label(r'disconnected/dbdisconn52.png', 52, 52, label_name=FORM_ICON_LABEL_NAME)
        self._conn_err_icon_label = self._produce_icon_label(r'connection-errors/dbconn_errors52.png', 52, 52, label_name=FORM_ICON_LABEL_NAME)
        self._connection_indicator = qtw.QStackedWidget()
        self._fill_connection_indicator_widget()

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self._db_connect_btn, stretch=0, alignment=qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        button_layout.addWidget(self._db_disconnect_btn, stretch=0, alignment=qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        button_layout.addWidget(self._connection_indicator, stretch=0, alignment=qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        button_layout.addStretch()

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(main_form)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _set_value_subscriptions(self):
        self._model.db_names_changed.connect(self._db_connection_names_changed)
        self._model.db_connect_status_changed.connect(self._connection_indicator.setCurrentIndex)
        self._model.db_threads_status_changed.connect(self._manage_action_buttons)

        self._db_conn_list.currentTextChanged.connect(self._model.set_current_connection)
        self._db_password_input.editingFinished.connect(
            lambda : self._model.set_password(self._db_password_input.text()))

    def _bind_buttons_to_commands(self):
        self._db_connect_btn.clicked.connect(self._model.connect_to_database)
        self._db_disconnect_btn.clicked.connect(self._model.disconnect_from_database)

    def _init_actions(self):
        self._model.get_connection_names()
        self._connection_indicator.setCurrentIndex(DB_DISCONNECTED)
        self._manage_action_buttons(DB_THREADS_FINISHED)

    def _db_connection_names_changed(self, names: list[str]):
        self._db_conn_list.clear()
        self._db_conn_list.addItems(names)

    def _fill_connection_indicator_widget(self):
        indicator_icons = {
            DB_CONNECTED: self._conn_icon_label
            ,DB_DISCONNECTED: self._disconn_icon_label
            ,DB_HAS_ERRORS: self._conn_err_icon_label }
        
        sorted_icons = sorted(indicator_icons.items())
        for key, value in sorted_icons:
            self._connection_indicator.addWidget(value)
            self._connection_indicator.addWidget(value)
            self._connection_indicator.addWidget(value)

    def _manage_action_buttons(self, status: int):
        connectable: bool = True if status == DB_THREADS_FINISHED else False
        
        self._db_connect_btn.setDisabled(not connectable)
        self._db_disconnect_btn.setDisabled(connectable)
      
        
if __name__ == '__main__':
    from lib.helpers.hp_visual_view_test_template import visual_test_preview
    visual_test_preview(VwDBConnectionConfig())