from PyQt5.QtGui import QValidator, QIntValidator, QDoubleValidator
import re

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
            try:
                if float(input_text) > self.top():
                    return QDoubleValidator.Invalid, input_text, pos
            except:
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
        octets = input_text.split('.')

        if len(octets) > 4:
            return QValidator.Invalid, input_text, pos
        
        for octet in octets:
            if octet == str():
                continue
            if bool(re.search(r'\s', octet)):
                return QValidator.Invalid, input_text, pos
            try:
                oct = int(octet)
                if oct < 0 or oct > 255:
                    return QValidator.Invalid, input_text, pos
            except:
                return QValidator.Invalid, input_text, pos
                        
        return QValidator.Acceptable, input_text, pos