from PyQt5 import QtGui
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.vw_1a_title_bar import VwTitleBar
from lib.views.vw_2_main import VwMain
from lib.helpers.constants.hp_gui_tem_names import *

INIT_POS_X = 100
INIT_POS_Y = 100
INIT_SIZE_X = 1000
INIT_SIZE_Y = 650


class VwMainWindow(qtw.QMainWindow):

    def __init__(self):
        super(VwMainWindow, self).__init__()
        self.setObjectName(MAIN_WINDOW_NAME)
        flags=qtc.Qt.WindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setGeometry(INIT_POS_X, INIT_POS_Y, INIT_SIZE_X, INIT_SIZE_Y)
    
        self.setMenuWidget(VwTitleBar(parent=self))
        self.setCentralWidget(VwMain(parent=self))

        self._create_grips()
        # below is needed to make the window moveable
        self._old_cursor_pos = None

        self.show()
    
    def _create_grips(self):
        self._grip_size = 12
        self._grips: list[qtw.QSizeGrip] = list()
        for i in range(4):
            grip = qtw.QSizeGrip(self)
            grip.resize(self._grip_size, self._grip_size)
            self._grips.append(grip)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        rect = self.rect()
        self._grips[1].move(rect.right() - self._grip_size, 0)
        self._grips[2].move(rect.right() - self._grip_size, rect.bottom() - self._grip_size)
        self._grips[3].move(0, rect.bottom() - self._grip_size)
             
        self.show()

        self._drag_start_position = self.frameGeometry().bottomRight()
        self._origin = self.frameGeometry().topLeft()

    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.MouseButton.LeftButton:
            self._old_cursor_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self._old_cursor_pos is not None:
            delta = event.globalPos() - self._old_cursor_pos
            self.move(self.pos() + delta)
            self._old_cursor_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self._old_cursor_pos = None