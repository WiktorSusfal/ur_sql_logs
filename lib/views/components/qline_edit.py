import PyQt5.QtWidgets as qtw

class URQLineEdit(qtw.QLineEdit):

    def __init__(self, object_name: str, input_mask: str, separator: str):
        super(URQLineEdit, self).__init__()

        self._filler = input_mask.split(';')[-1]
        self._separator = separator
        self.setObjectName(object_name)
        self.setInputMask(input_mask)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        
        if self._get_value_length() == 0:
            self.setCursorPosition(0)

    def _get_value_length(self):
        v = [char for char in self.text() if char != self._filler and char != self._separator]
        return len(v)
        