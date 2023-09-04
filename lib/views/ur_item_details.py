import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.helpers.gui_tem_names import *
from lib.views.components.base_view import URLoggerBaseView

class URItemDetails(URLoggerBaseView):

    def __init__(self):
        super(URItemDetails, self).__init__()
        self.setObjectName(UR_ITEM_DETAILS_VIEW_NAME)
        
        self._robot_name_input = qtw.QLineEdit()
        self._robot_name_input.setObjectName(FORM_INPUT_NAME)
        self._ip_address_input = qtw.QLineEdit()
        self._ip_address_input.setObjectName(FORM_INPUT_NAME)
        self._port_number_input = qtw.QLineEdit()
        self._port_number_input.setObjectName(FORM_INPUT_NAME)
        self._refresh_freq_input = qtw.QLineEdit()
        self._refresh_freq_input.setObjectName(FORM_INPUT_NAME)
        
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
            ,self._refresh_freq_input)
        
        self._robot_icon_label = self._produce_icon_label(r'robot/industrial-robot256.png', 200, 200)
        self._recent_messages_table = qtw.QTableView()

        self._connect_button = self._produce_button(button_label='Connect'
                                                    , button_name=ACTION_BUTTON_NAME)
        self._disconnect_button = self._produce_button(button_label='Disconnect'
                                                    , button_name=ACTION_BUTTON_NAME)

        details_layout = qtw.QHBoxLayout()
        details_layout.addLayout(main_form)
        details_layout.addWidget(self._robot_icon_label, stretch = 0)

        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self._connect_button, stretch = 0, alignment = qtc.Qt.AlignLeft)
        buttons_layout.addWidget(self._disconnect_button, stretch = 0, alignment = qtc.Qt.AlignLeft)
        buttons_layout.addStretch()

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(details_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self._recent_messages_table)

        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass
    
    def _init_actions(self):
        pass
    
    def _set_value_subscriptions(self):
        pass
            

if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(URItemDetails())