import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import USLBaseView
from lib.view_models.vm_4a_robot_connection import VmRobotConnection
from lib.helpers.constants.hp_gui_tem_names import *


class VwListItem(USLBaseView):

    def __init__(self, model: VmRobotConnection, parent = None):
        super(VwListItem, self).__init__(parent)
        self.setObjectName(UR_LIST_ITEM_VIEW_NAME)
        self.model = model

        self._robot_icon_label = self._produce_icon_label(r'robot/industrial-robot.png', 50, 50, label_name=LIST_ITEM_ICON_LABEL_NAME)
        self._on_icon_label = self._produce_icon_label(r'connected/conn48.png', 60, 20, label_name=LIST_ITEM_ICON_LABEL_NAME)
        self._off_icon_label = self._produce_icon_label(r'disconnected/disconn48.png', 60, 20, label_name=LIST_ITEM_ICON_LABEL_NAME)
        self._mail_icon_label = self._produce_icon_label(r'mail/mail.png', 24, 24, label_name=LIST_ITEM_ICON_LABEL_NAME)
        
        self._in_db_icon_label = self._produce_icon_label(r'connected/dbcon52.png', 24, 24
                                                          , label_name=LIST_ITEM_ICON_LABEL_NAME
                                                          , tooltip='Model up to date with database')
        self._not_in_db_icon_label = self._produce_icon_label(r'disconnected/dbdisconn52.png', 24, 24
                                                              , label_name=LIST_ITEM_ICON_LABEL_NAME
                                                              , tooltip='Model not exists in database')
        self._differences_db_icon_label = self._produce_icon_label(r'connection-errors/changes_in_db.png', 24, 24
                                                              , label_name=LIST_ITEM_ICON_LABEL_NAME
                                                              , tooltip='Model has not saved changes')

        self._title_label = qtw.QLabel(self.model.robot_connection_name)
        self._title_label.setObjectName(LIST_ITEM_TITLE_LABEL_NAME)

        self._message_counter_label = qtw.QLabel("0")
        self._message_counter_label.setObjectName(LIST_ITEM_DETAIL_LABEL_NAME)

        self._connection_indicator = qtw.QStackedWidget()
        self._connection_indicator.addWidget(self._off_icon_label)
        self._connection_indicator.addWidget(self._on_icon_label)

        self._db_saved_indicator = qtw.QStackedWidget()
        self._db_saved_indicator.addWidget(self._not_in_db_icon_label)
        self._db_saved_indicator.addWidget(self._in_db_icon_label)
        self._db_saved_indicator.addWidget(self._differences_db_icon_label)

        details_layout = qtw.QHBoxLayout()
        details_layout.addWidget(self._connection_indicator, stretch = 0, alignment = qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        details_layout.addWidget(self._mail_icon_label, stretch = 0, alignment = qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        details_layout.addWidget(self._message_counter_label, stretch = 0, alignment = qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        details_layout.addWidget(self._db_saved_indicator, stretch = 0, alignment = qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)

        info_layout = qtw.QVBoxLayout()
        info_layout.addWidget(self._title_label, stretch = 0, alignment = qtc.Qt.AlignTop)
        info_layout.addLayout(details_layout, stretch = 0)

        main_layout = qtw.QHBoxLayout()
        main_layout.addWidget(self._robot_icon_label, stretch = 0, alignment = qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        main_layout.addLayout(info_layout, stretch = 0)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass

    def _set_value_subscriptions(self):
        self.model.connection_name_changed.connect(self._title_label.setText)
        self.model.message_counter_changed.connect(
                lambda cnt: self._message_counter_label.setText(str(cnt))
            )
        self.model.connection_status_changed.connect(
                lambda status: self._connection_indicator.setCurrentIndex(int(status))
            )
        self.model.db_saved_status_changed.connect(self._db_saved_indicator.setCurrentIndex)

    def _init_actions(self):
        pass


if __name__ == '__main__':
    from lib.helpers.utils.hp_visual_view_test_template import visual_test_preview
    model = VmRobotConnection()
    visual_test_preview(VwListItem(model))