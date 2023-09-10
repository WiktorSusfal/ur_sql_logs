from PyQt5.QtCore import QObject, pyqtSignal


class ApplicationHome(QObject):

    current_connection_changed = pyqtSignal()

    def __init__(self):
        super(ApplicationHome, self).__init__()
        
        self._ur_connections_list = list()