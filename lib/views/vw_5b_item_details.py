import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import USLBaseView
from lib.views.components.validators import USLIntValidator, USLDoubleValidator, USLIPAddressValidator

from lib.helpers.resources.hp_view_models_manager import HpViewModelsManager
from lib.helpers.constants.hp_gui_tem_names import *


class VwItemDetails(USLBaseView):

    def __init__(self, parent=None):
        super(VwItemDetails, self).__init__(parent=parent)
        self.setObjectName(UR_ITEM_DETAILS_VIEW_NAME)
        self._model = HpViewModelsManager.robot_details_view_model
        
        self._robot_name_input = self._produce_line_edit(FORM_INPUT_NAME)
        self._ip_address_input = self._produce_line_edit(FORM_INPUT_NAME, USLIPAddressValidator(self))
        self._port_number_input = self._produce_line_edit(FORM_INPUT_NAME, USLIntValidator(1, 65535, self))
        self._read_freq_input = self._produce_line_edit(FORM_INPUT_NAME, USLDoubleValidator(0.0, 360.0, 1, self))

        main_form = qtw.QFormLayout()
        main_form.addRow(
            self._produce_named_label("Unique Name: ", FORM_LABEL_NAME)
            ,self._robot_name_input)
        main_form.addRow(
            self._produce_named_label("IP Address: ", FORM_LABEL_NAME)
            ,self._ip_address_input)
        main_form.addRow(
            self._produce_named_label("Port Number: ", FORM_LABEL_NAME)
            ,self._port_number_input)
        main_form.addRow(
            self._produce_named_label("Read Frequency: ", FORM_LABEL_NAME)
            ,self._read_freq_input)
        
        self._robot_icon_label = self._produce_icon_label(r'robot/industrial-robot256.png', 200, 200)
        self._recent_messages_table = qtw.QTableView()

        self._save_button = self._produce_button(icon_rel_path=r'save/save24.png', icon_size=20
                                                 , button_name=ACTION_BUTTON_NAME)
        self._refresh_button = self._produce_button(icon_rel_path=r'refresh/refresh24.png', icon_size=20
                                                    , button_name=ACTION_BUTTON_NAME)
        self._connect_button = self._produce_button(button_label='Connect'
                                                    , button_name=ACTION_BUTTON_NAME)
        self._disconnect_button = self._produce_button(button_label='Disconnect'
                                                       , button_name=ACTION_BUTTON_NAME)

        details_layout = qtw.QHBoxLayout()
        details_layout.addLayout(main_form)
        details_layout.addWidget(self._robot_icon_label, stretch = 0)

        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self._save_button, stretch = 0)
        buttons_layout.addWidget(self._refresh_button, stretch = 0)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._connect_button, stretch = 0, alignment = qtc.Qt.AlignRight)
        buttons_layout.addWidget(self._disconnect_button, stretch = 0, alignment = qtc.Qt.AlignRight)

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(details_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self._recent_messages_table)

        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        self._refresh_button.clicked.connect(self._model.update_interface_data)
        self._save_button.clicked.connect(self._model.save_interface_data)
        self._connect_button.clicked.connect(self._model.robot_connect)
        self._disconnect_button.clicked.connect(self._model.robot_disconnect)
    
    def _init_actions(self):
        pass
    
    def _set_value_subscriptions(self):
        self._model.name_changed.connect(self._robot_name_input.setText)
        self._model.ip_changed.connect(self._ip_address_input.setText)
        self._model.port_changed.connect(self._port_number_input.setText)
        self._model.read_freq_changed.connect(self._read_freq_input.setText)

        self._robot_name_input.editingFinished.connect(
            lambda : self._model.set_name(self._robot_name_input.text()))
        self._ip_address_input.editingFinished.connect(
            lambda : self._model.set_ip_address(self._ip_address_input.text()))
        self._port_number_input.editingFinished.connect(
            lambda : self._model.set_port(self._port_number_input.text()))
        self._read_freq_input.editingFinished.connect(
            lambda: self._model.set_read_frequency(self._read_freq_input.text()))


if __name__ == '__main__':
    from lib.helpers.utils.hp_visual_view_test_template import visual_test_preview
    visual_test_preview(VwItemDetails())