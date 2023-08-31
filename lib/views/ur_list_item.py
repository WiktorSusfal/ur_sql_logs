import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import URLoggerBaseView
from lib.helpers.gui_tem_names import *

DISCONNECTED_MESSAGE = "Disconnected"
CONNECTED_MESSAGE = "Connected"

class URListItem(URLoggerBaseView):

    def __init__(self, id: str, title: str):
        super(URListItem, self).__init__()
        self.setObjectName(UR_LIST_ITEM_VIEW_NAME)
        self.id = id

        self._robot_icon_label = self._produce_icon_label(r'robot/industrial-robot.png', 64, 64)
        self._on_icon_label = self._produce_icon_label(r'onoff/on.png', 32, 32)
        self._off_icon_label = self._produce_icon_label(r'onoff/off.png', 32, 32)
        self._mail_icon_label = self._produce_icon_label(r'mail/mail.png', 32, 32)
        
        self._title_label = qtw.QLabel(title)
        self._title_label.setObjectName(LIST_ITEM_TITLE_LABEL_NAME)

        self._connection_status_label = qtw.QLabel(DISCONNECTED_MESSAGE)
        self._connection_status_label.setObjectName(LIST_ITEM_DETAIL_LABEL_NAME)
        self._message_counter_label = qtw.QLabel("0")
        self._message_counter_label.setObjectName(LIST_ITEM_DETAIL_LABEL_NAME)

        self._connection_indicator = qtw.QStackedWidget()
        self._connection_indicator.addWidget(self._off_icon_label)
        self._connection_indicator.addWidget(self._on_icon_label)

        details_layout = qtw.QHBoxLayout()
        details_layout.addWidget(self._connection_indicator, stretch = 0, alignment = qtc.Qt.AlignLeft)
        details_layout.addWidget(self._connection_status_label, stretch = 0, alignment = qtc.Qt.AlignLeft)
        details_layout.addWidget(self._mail_icon_label, stretch = 0, alignment = qtc.Qt.AlignLeft)
        details_layout.addWidget(self._message_counter_label, stretch = 0, alignment = qtc.Qt.AlignLeft)

        info_layout = qtw.QVBoxLayout()
        info_layout.addWidget(self._title_label, stretch = 0, alignment = qtc.Qt.AlignTop)
        info_layout.addLayout(details_layout, stretch = 0)

        main_layout = qtw.QHBoxLayout()
        main_layout.addWidget(self._robot_icon_label, stretch = 0, alignment = qtc.Qt.AlignLeft)
        main_layout.addLayout(info_layout, stretch = 0)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass

    def _set_value_subscriptions(self):
        pass

    def _init_actions(self):
        pass


if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(URListItem("Test item"))