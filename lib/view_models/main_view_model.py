from PyQt5.QtCore import QObject, pyqtSignal

HOME_VIEW_INDEX = 0
DB_CONNECTION_VIEW_INDEX = 1
HELP_VIEW_INDEX = 2

class URMainViewModel(QObject):

    content_view_index_changed = pyqtSignal(int)

    def __init__(self):
        super(URMainViewModel, self).__init__()
        self._current_view_index = 0

    @property
    def current_view_index(self) -> int:
        return self._current_view_index
    
    @current_view_index.setter
    def current_view_index(self, index: int): 
        self._current_view_index = index
        self.content_view_index_changed.emit(index)
        
    def set_home_view(self):
        self.current_view_index = HOME_VIEW_INDEX

    def set_db_connection_view(self):
        self.current_view_index = DB_CONNECTION_VIEW_INDEX

    def set_help_view(self):
        self.current_view_index = HELP_VIEW_INDEX