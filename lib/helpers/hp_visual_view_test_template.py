import PyQt5.QtWidgets as qtw
import sys as sys

from lib.helpers.hp_resources_manager import HpResourcesManager

_test_view_app = qtw.QApplication(sys.argv)
_test_view_app.setStyleSheet(HpResourcesManager.get_styles_code())

def visual_test_preview(target_widget: qtw.QWidget):
    
    class HpVisualTestWidget(qtw.QMainWindow):

        def __init__(self, target_widget: qtw.QWidget):
            super(HpVisualTestWidget, self).__init__()
            
            self.setWindowTitle("Visual Test View")
            self.setCentralWidget(target_widget)

            self.show()

    app_main_gui = HpVisualTestWidget(target_widget)
    sys.exit(_test_view_app.exec_())


if __name__ == '__main__':
    visual_test_preview(qtw.QLabel('Test Label Widget'))