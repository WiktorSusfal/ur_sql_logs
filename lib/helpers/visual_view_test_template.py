import PyQt5.QtWidgets as qtw
import sys as sys
import pathlib as pth

from lib.helpers.styles_code_manager import ResourcesManager

_test_view_app = qtw.QApplication(sys.argv)
_test_view_app.setStyleSheet(ResourcesManager.get_styles_code())

def visual_test_preview(target_widget: qtw.QWidget):
    
    class VisualTestWidget(qtw.QMainWindow):

        def __init__(self, target_widget: qtw.QWidget):
            super(VisualTestWidget, self).__init__()
            
            self.setWindowTitle("Visual Test View")
            self.setCentralWidget(target_widget)

            self.show()

    app_main_gui = VisualTestWidget(target_widget)
    sys.exit(_test_view_app.exec_())


if __name__ == '__main__':
    visual_test_preview(qtw.QLabel('Test Label Widget'))