import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import USLBaseView

from lib.helpers.constants.hp_gui_tem_names import *


class VwItemDetailsPlaceholder(USLBaseView):

    def __init__(self, parent=None):
        super(VwItemDetailsPlaceholder, self).__init__(parent=parent)
        self.setObjectName(UR_ITEM_DETAILS_PLACEHOLDER_VIEW_NAME)

        self._robot_icon_label = self._produce_icon_label(r'robot/industrial-robot256.png', 256, 256)
        self._info_label = qtw.QLabel('No item selected')
        self._info_label.setObjectName(HINT_LABEL_NAME)
        main_layout = qtw.QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(self._robot_icon_label, stretch=0, alignment=qtc.Qt.AlignVCenter | qtc.Qt.AlignHCenter)
        main_layout.addWidget(self._info_label, stretch=0, alignment=qtc.Qt.AlignVCenter | qtc.Qt.AlignHCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self._setup()
        self.show()

    def _set_value_subscriptions(self):
        pass

    def _bind_buttons_to_commands(self):
        pass

    def _init_actions(self):
        pass


if __name__ == '__main__':
    from lib.helpers.utils.hp_visual_view_test_template import visual_test_preview
    visual_test_preview(VwItemDetailsPlaceholder())