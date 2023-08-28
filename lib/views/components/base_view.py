import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from abc import ABC, abstractmethod, ABCMeta

from lib.helpers.styles_code_manager import ResourcesManager


class URLoggerBaseViewMeta(ABCMeta, type(qtw.QWidget)):
    pass


class URLoggerBaseView(ABC, qtw.QWidget,  metaclass=URLoggerBaseViewMeta):

    def __init__(self):
        super().__init__()
        super(ABC, self).__init__()

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

    def _produce_icon_button(self, icon_rel_path: str, button_name: str = None, icon_size: int = None) -> qtw.QPushButton:
        icon = qtg.QIcon(ResourcesManager.get_icon_abs_path(icon_rel_path))
        button = qtw.QPushButton()
        button.setIcon(icon)

        if button_name:
            button.setObjectName(button_name)
        
        if icon_size:
            button.setIconSize(qtc.QSize(icon_size, icon_size))

        return button
    
    def _produce_icon_label(self, icon_rel_path: str, size_x: int, size_y: int, label_name: str = None) -> qtw.QLabel:
        icon = qtg.QIcon(ResourcesManager.get_icon_abs_path(icon_rel_path))
        icon_label = qtw.QLabel()
        icon_label.setPixmap(icon.pixmap(size_x, size_y))

        if label_name:
            icon_label.setObjectName(label_name)

        return icon_label
