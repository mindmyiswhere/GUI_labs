from PyQt5.QtCore import QObject, pyqtSignal

class RublesModel(QObject):
    valueChanged = pyqtSignal(float)

    def __init__(self):
        super().__init__()

    def get_value(self):
        return self._value

    def set_value(self, val):
        if abs(val - self._value) > 0.001:
            self._value = val
            self.valueChanged.emit(val)