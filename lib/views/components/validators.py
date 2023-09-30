from PyQt5.QtGui import QValidator, QIntValidator, QDoubleValidator


class USLIntValidator(QIntValidator):
    
    def validate(self, input_text:str, pos:int):
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
    
    def validate(self, input_text:str, pos:int):
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
    

class USLIPAddressValidator(QValidator):
    
    def validate(self, input_text: str, pos: int):

        char, prev_char, prev_2_char, dot_count = None, None, None, 0
        for i, c in enumerate(input_text):
            prev_2_char = prev_char
            prev_char = char
            char = c

            if not (char.isnumeric() or char == '.'):
                return QValidator.Invalid, input_text, pos
            
            if i == 0 and (char == '0' or char == '.'):
                return QValidator.Invalid, input_text, pos
            
            if i > 1 and char == '0' and prev_char == '0' and prev_2_char == '.':
                return QValidator.Invalid, input_text, pos
            
            if i > 1 and char not in ('0', '.') and prev_char == '0' and prev_2_char == '.':
                return QValidator.Invalid, input_text, pos
            
            if i > 1 and char == '.' and prev_char == '.':
                return QValidator.Invalid, input_text, pos
            
            if char == '.':
                dot_count += 1
                if dot_count > 3:
                    return QValidator.Invalid, input_text, pos
                
        octets = input_text.split('.')
        for octet in octets:
            if len(octet) > 0 and int(octet) > 255:
                return QValidator.Invalid, input_text, pos
                
        return QValidator.Acceptable, input_text, pos