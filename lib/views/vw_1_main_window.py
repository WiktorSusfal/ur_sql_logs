import PyQt5.QtWidgets as qtw

from lib.views.vw_2_main import VwMain
from lib.helpers.hp_gui_tem_names import *

INIT_POS_X = 100
INIT_POS_Y = 100
INIT_SIZE_X = 1000
INIT_SIZE_Y = 600


class VwMainWindow(qtw.QMainWindow):

    def __init__(self):
        super(VwMainWindow, self).__init__()
        self.setObjectName(MAIN_WINDOW_NAME)
        self.setWindowTitle('UR SQL Logger')
        self.setGeometry(INIT_POS_X, INIT_POS_Y, INIT_SIZE_X, INIT_SIZE_Y)

        self.setCentralWidget(VwMain(parent=self))

        self.show()