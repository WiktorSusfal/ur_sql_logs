import PyQt5.QtWidgets as qtw

from lib.helpers.gui_tem_names import *

INIT_POS_X = 100
INIT_POS_Y = 100
INIT_SIZE_X = 800
INIT_SIZE_Y = 600


class URLoggerMainView(qtw.QMainWindow):

    def __init__(self):
        super(URLoggerMainView, self).__init__()
        self.setWindowTitle('UR SQL Logger')
        self.setGeometry(INIT_POS_X, INIT_POS_Y, INIT_SIZE_X, INIT_SIZE_Y)

        self._main_layout = qtw.QGridLayout()
        self._main_layout.setObjectName(MAIN_LAYOUT_NAME)

        self._central_widget = qtw.QWidget()
        self._central_widget.setLayout(self._main_layout)
        self.setCentralWidget(self._central_widget)

        self.show()






    
