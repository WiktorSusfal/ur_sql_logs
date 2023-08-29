import sys
from PyQt5.QtWidgets import QApplication

from lib.views.main_window import URLoggerMainWindow
from lib.helpers.styles_code_manager import ResourcesManager


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(ResourcesManager.get_styles_code())
    main_view = URLoggerMainWindow()
    sys.exit(app.exec_())