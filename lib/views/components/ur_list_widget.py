import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.helpers.gui_tem_names import *


class URListWidget(qtw.QListWidget):
    def __init__(self):
        super(URListWidget, self).__init__()

        self.caption_label = qtw.QLabel("No connections added", self)
        self.caption_label.setAlignment(qtc.Qt.AlignTop | qtc.Qt.AlignHCenter)
        self.caption_label.setObjectName(HINT_LABEL_NAME)
        self.caption_label.hide()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            self.caption_label.setGeometry(self.rect())
            self.caption_label.show()
        else:
            self.caption_label.hide()
