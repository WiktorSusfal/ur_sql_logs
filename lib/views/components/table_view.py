import PyQt5.QtWidgets as qtw

from lib.view_models.vm_4b_message_data import VmMessageData


class USLTableView(qtw.QTableView):
        
    def __init__(self, parent, model: VmMessageData = None):
        super(USLTableView, self).__init__(parent=parent)

        self.horizontalHeader().setSectionsClickable(False)
        self.verticalHeader().setSectionsClickable(False)
        self.verticalHeader().setHidden(True)
        self.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
    
        self._table_model: VmMessageData = None
        if model:
            self._set_table_model(model)

    def _set_table_model(self, model: VmMessageData):
        if self._table_model:
            raise Exception('Table view model already set - cannot be reset')
        
        self._table_model = model
        self._table_model.setParent(self)
        self.setModel(self._table_model)

        self._table_model.init_message_added.connect(
            lambda status : self.resizeColumnsToContents())