import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QValidator

from lib.helpers.constants.hp_gui_tem_names import *


class USLLineEdit(qtw.QLineEdit):

    def __init__(self, name: str, validator: QValidator = None):
        super(USLLineEdit, self).__init__()

        usl_locale = qtc.QLocale(qtc.QLocale.English, qtc.QLocale.UnitedStates)
        usl_locale.setNumberOptions(qtc.QLocale.RejectGroupSeparator)

        self.setObjectName(name)
        if validator:
            validator.setLocale(usl_locale)
            self.setValidator(validator)

        self._changes_active = False
        
        self._changes_indicator = qtw.QLabel("*")
        self._changes_indicator.setParent(self)
        self._changes_indicator.setAlignment(qtc.Qt.AlignRight | qtc.Qt.AlignTop)
        self._changes_indicator.setObjectName(CHANGES_INDICATOR_LABEL_NAME)

    def paintEvent(self, event):
        super().paintEvent(event)
        self._changes_indicator.setGeometry(self.rect())
        
        if self._changes_active:
            self._changes_indicator.show()
        else: 
            self._changes_indicator.hide()

    def set_changes_active(self, changes_state: bool):
        self._changes_active = changes_state
        self.repaint()

if __name__ == '__main__':
    from lib.helpers.utils.hp_visual_view_test_template import visual_test_preview
    visual_test_preview(USLLineEdit())