"""Contains method which displays any PyQt5 widget object inside new window 
with all predefined qss styles active (stored in resources folder)."""

import PyQt5.QtWidgets as qtw
import sys as sys

from lib.helpers.resources.hp_resources_manager import HpResourcesManager

_test_view_app = qtw.QApplication(sys.argv)
_test_view_app.setStyleSheet(HpResourcesManager.get_styles_code())

def visual_test_preview(target_widget: qtw.QWidget):
    """Displays any PyQt5 widget object inside new window 
        with all predefined qss styles active (stored in resources folder)."""
    
    class HpVisualTestWidget(qtw.QMainWindow):

        def __init__(self, target_widget: qtw.QWidget):
            super(HpVisualTestWidget, self).__init__()
            
            self.setWindowTitle("Visual Test View")
            self.setCentralWidget(target_widget)

            self.show()

    app_main_gui = HpVisualTestWidget(target_widget)
    sys.exit(_test_view_app.exec_())