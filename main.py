import sys
from PyQt5.QtWidgets import QApplication

from lib.views.vw_1_main_window import VwMainWindow
from lib.helpers.hp_resources_manager import HpResourcesManager


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(HpResourcesManager.get_styles_code())
    main_view = VwMainWindow()  
    sys.exit(app.exec_())