from PyQt5.QtCore import QObject


class BaseViewModel(QObject):

    def __init__(self):
        super(BaseViewModel, self).__init__()

    @staticmethod
    def observable_property(property_name: str, signal_name: str):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    target_object, setter_value = args[0], args[1]
                    target_property = getattr(target_object, property_name)
                    
                    if setter_value != target_property:
                        func(*args, **kwargs)
                        target_signal = getattr(target_object, signal_name)
                        target_signal.emit(setter_value)
                
                return wrapper
            return decorator