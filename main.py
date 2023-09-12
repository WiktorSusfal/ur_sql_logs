import sys
from PyQt5.QtWidgets import QApplication

from lib.views.v_1_main_window import MainWindow
from lib.helpers.resources_manager import ResourcesManager


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(ResourcesManager.get_styles_code())
    main_view = MainWindow()  
    sys.exit(app.exec_())