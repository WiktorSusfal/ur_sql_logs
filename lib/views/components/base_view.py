import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from abc import ABC, abstractmethod, ABCMeta

from lib.helpers.resources.hp_resources_manager import HpResourcesManager
from lib.helpers.constants.hp_gui_tem_names import *


class _USLBaseViewMeta(ABCMeta, type(qtw.QWidget)):
    pass


class USLBaseView(ABC, qtw.QWidget,  metaclass=_USLBaseViewMeta):

    usl_locale = qtc.QLocale(qtc.QLocale.English, qtc.QLocale.UnitedStates)
    usl_locale.setNumberOptions(qtc.QLocale.RejectGroupSeparator)

    def __init__(self, parent=None):
        qtw.QWidget.__init__(self, parent=parent)
        ABC.__init__(self)
        self.setObjectName(CUSTOM_VIEW_WIDGET_NAME)
        self.setAttribute(qtc.Qt.WA_StyledBackground)

    @abstractmethod
    def _set_value_subscriptions(self):
        pass

    @abstractmethod
    def _bind_buttons_to_commands(self):
        pass

    @abstractmethod
    def _init_actions(self):
        pass

    def _setup(self):
        self._set_value_subscriptions()
        self._bind_buttons_to_commands()
        self._init_actions()

    def _produce_button(self, icon_rel_path: str = None, icon_size: int = None, button_name: str = None, button_label: str = None) -> qtw.QPushButton:
        button = qtw.QPushButton()
        button.setCursor(qtc.Qt.PointingHandCursor)

        if icon_rel_path:
            icon = qtg.QIcon(HpResourcesManager.get_icon_abs_path(icon_rel_path))
            button.setIcon(icon)
            if icon_size:
                button.setIconSize(qtc.QSize(icon_size, icon_size))

        if button_name:
            button.setObjectName(button_name)

        if button_label:
            button.setText(button_label)

        return button
    
    def _produce_icon_label(self, icon_rel_path: str, size_x: int, size_y: int
                            , label_name: str = None, tooltip: str = None) -> qtw.QLabel:
        icon = qtg.QIcon(HpResourcesManager.get_icon_abs_path(icon_rel_path))
        icon_label = qtw.QLabel()
        icon_label.setPixmap(icon.pixmap(size_x, size_y))

        if label_name:
            icon_label.setObjectName(label_name)

        if tooltip:
            icon_label.setToolTip(tooltip)

        return icon_label
    
    def _produce_named_label(self, content: str, name: str) -> qtw.QLabel:
        label = qtw.QLabel(content)
        label.setObjectName(name)
        return label
    
    def _produce_line_edit(self, name: str, validator: qtg.QValidator = None, echo_mode: int = None) -> qtw.QLineEdit:
        line_edit = qtw.QLineEdit()
        line_edit.setObjectName(name)

        if echo_mode:
            line_edit.setEchoMode(echo_mode)

        if validator:
            validator.setLocale(self.usl_locale)
            line_edit.setValidator(validator)

        return line_edit