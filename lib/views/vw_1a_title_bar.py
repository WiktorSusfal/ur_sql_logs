import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import USLBaseView

from lib.helpers.constants.hp_gui_tem_names import *


class VwTitleBar(USLBaseView):
    def __init__(self, parent):
        super(VwTitleBar, self).__init__(parent=parent)
        self.setObjectName(TITLE_BAR_NAME)

        self._app_icon = self._produce_icon_label(r'robot/industrial-robot.png', 24, 24, label_name=TITLE_ICON_LABEL_NAME)
        self._title_label = self._produce_named_label('UR SQL Logger', name=TITLE_LABEL_NAME)
     
        self._minimize_button = self._produce_button(icon_rel_path=r'utils/minimize.png', icon_size=24, button_name=TITLEBAR_BUTTON_NAME)
        self._maximize_button = self._produce_button(icon_rel_path=r'utils/maximize.png', icon_size=24, button_name=TITLEBAR_BUTTON_NAME)
        self._close_button = self._produce_button(icon_rel_path=r'utils/close.png', icon_size=24, button_name=TITLEBAR_BUTTON_NAME)

        self._main_layout = qtw.QHBoxLayout()
        self._main_layout.addWidget(self._app_icon, alignment=qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter, stretch=0)
        self._main_layout.addWidget(self._title_label, alignment=qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter, stretch=0)
        self._main_layout.addStretch()
        self._main_layout.addWidget(self._minimize_button, alignment=qtc.Qt.AlignRight | qtc.Qt.AlignVCenter, stretch=0)
        self._main_layout.addWidget(self._maximize_button, alignment=qtc.Qt.AlignRight | qtc.Qt.AlignVCenter, stretch=0)
        self._main_layout.addWidget(self._close_button, alignment=qtc.Qt.AlignRight | qtc.Qt.AlignVCenter, stretch=0)
        
        self.setLayout(self._main_layout)
        self._setup()

    def _minimize_window(self):
        if self.parentWidget().isMaximized():
            self.parentWidget().showNormal()
        self.parentWidget().showMinimized()

    def _maximize_window(self):
        if self.parentWidget().isMaximized():
            self.parentWidget().showNormal()
        else:
            self.parentWidget().showMaximized()

    def _close_window(self):
        self.parentWidget().close()

    def _set_value_subscriptions(self):
        pass

    def _bind_buttons_to_commands(self):
        self._minimize_button.clicked.connect(self._minimize_window)
        self._maximize_button.clicked.connect(self._maximize_window)
        self._close_button.clicked.connect(self._close_window)

    def _init_actions(self):
        pass