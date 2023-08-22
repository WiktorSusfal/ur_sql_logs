import PyQt5.QtWidgets as qtw
import sys as sys

_test_view_app = qtw.QApplication(sys.argv)

def visual_test_preview(target_widget: qtw.QWidget):
    
    class VisualTestWidget(qtw.QMainWindow):

        def __init__(self, target_widget: qtw.QWidget):
            super(VisualTestWidget, self).__init__()
            
            self.setWindowTitle("Visual Test View")

            self.main_layout = qtw.QVBoxLayout()
            self.main_layout.addWidget(target_widget)
            
            central_widget = qtw.QWidget()
            central_widget.setLayout(self.main_layout)
            self.setCentralWidget(central_widget)

            self.show()

    app_main_gui = VisualTestWidget(target_widget)
    sys.exit(_test_view_app.exec_())

if __name__ == '__main__':
    visual_test_preview(qtw.QLabel('Test Label Widget'))