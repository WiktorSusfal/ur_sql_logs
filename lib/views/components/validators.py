from PyQt5.QtGui import QIntValidator, QDoubleValidator


class USLIntValidator(QIntValidator):
    
    def validate(self, input_text, pos):
        state, input_text, pos = super().validate(input_text, pos)
        
        if state == QIntValidator.Intermediate and len(input_text) > 0:
            if int(input_text) > self.top():
                return QIntValidator.Invalid, input_text, pos
            
        if state != QIntValidator.Invalid:
            if input_text.startswith("00"):
                return QIntValidator.Invalid, input_text, pos
                
            if input_text.startswith("0") and self.bottom() > 0:
                return QIntValidator.Invalid, input_text, pos
                
        return state, input_text, pos
    

class USLDoubleValidator(QDoubleValidator):
    
    def validate(self, input_text, pos):
        state, input_text, pos = super().validate(input_text, pos)
        
        if state == QDoubleValidator.Intermediate and len(input_text) > 0:  
            if float(input_text) > self.top():
                return QDoubleValidator.Invalid, input_text, pos
            
        if state != QDoubleValidator.Invalid:
            if input_text.startswith("00") or input_text.startswith("."):
                return QIntValidator.Invalid, input_text, pos
                
            if input_text.startswith("0") and self.bottom() > 0:
                return QIntValidator.Invalid, input_text, pos
            
            if len(input_text) > 1 and input_text.startswith("0") and input_text[1] != '.':
                return QIntValidator.Invalid, input_text, pos
          
        return state, input_text, pos