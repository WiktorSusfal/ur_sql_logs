from PyQt5.QtWidgets import QScrollBar

from lib.helpers.gui_tem_names import *


class CustomScrollBar(QScrollBar):
    def __init__(self):
        super(CustomScrollBar, self).__init__()
        self.setObjectName(CUSTOM_SCROLLBAR_NAME)
        