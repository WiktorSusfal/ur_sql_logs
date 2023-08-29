import PyQt5.QtWidgets as qtw

from lib.views.main_view import URLoggerMainView

INIT_POS_X = 100
INIT_POS_Y = 100
INIT_SIZE_X = 1000
INIT_SIZE_Y = 600


class URLoggerMainWindow(qtw.QMainWindow):

    def __init__(self):
        super(URLoggerMainWindow, self).__init__()
        self.setWindowTitle('UR SQL Logger')
        self.setGeometry(INIT_POS_X, INIT_POS_Y, INIT_SIZE_X, INIT_SIZE_Y)

        self.setCentralWidget(URLoggerMainView())

        self.show()