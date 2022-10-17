from ctypes import c_double, c_float
import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from ui_float import Ui_MainWindow
from utils import bin_str_to_ctypes, check_system, ctypes_to_str, hex_str_to_ctypes

LINE_VALUE = 0
LINE_BIN = 1
LINE_HEX = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        check_system()

        self._ui.lineFloat.setText('0.0')
        self._ui.lineDouble.setText('0.0')

    def setBlock(self, block: bool):
        self._ui.lineFloat.blockSignals(block)
        self._ui.lineDouble.blockSignals(block)
        self._ui.lineFloatBin.blockSignals(block)
        self._ui.lineDoubleBin.blockSignals(block)
        self._ui.lineFloatHex.blockSignals(block)
        self._ui.lineDoubleHex.blockSignals(block)

    def setFloat(self, value: c_float, event_type: int = LINE_VALUE):
        self.setBlock(True)
        bin_text, hex_text = ctypes_to_str(value)
        if event_type != LINE_VALUE:
            self._ui.lineFloat.setText(str(value.value))
        if event_type != LINE_BIN:
            self._ui.lineFloatBin.setText(bin_text)
        if event_type != LINE_HEX:
            self._ui.lineFloatHex.setText(hex_text)
        self._ui.lcdFloatSign.display(bin_text[0])
        self._ui.lcdFloatExponent.display(bin_text[1:9])
        self._ui.lcdFloatMantissa.display(bin_text[9:])
        self._ui.lineFloatStored.setText(str(value.value))
        self.setBlock(False)

    def setDouble(self, value: c_double, event_type: int = LINE_VALUE):
        self.setBlock(True)
        bin_text, hex_text = ctypes_to_str(value)
        if event_type != LINE_VALUE:
            self._ui.lineDouble.setText(str(value.value))
        if event_type != LINE_BIN:
            self._ui.lineDoubleBin.setText(bin_text)
        if event_type != LINE_HEX:
            self._ui.lineDoubleHex.setText(hex_text)
        self._ui.lcdDoubleSign.display(bin_text[0])
        self._ui.lcdDoubleExponent.display(bin_text[1:12])
        self._ui.lcdDoubleMantissa.display(bin_text[12:])
        self._ui.lineDoubleStored.setText(str(value.value))
        self.setBlock(False)

    @Slot(str)
    def floatChange(self, text: str):
        value = None
        try:
            value = c_float(float(text))
        except ValueError:
            pass
        if value is not None:
            self.setFloat(value, LINE_VALUE)

    @Slot(str)
    def floatChangeBin(self, text: str):
        if len(text) != 35:
            return None
        value = None
        try:
            value = bin_str_to_ctypes(text, c_float)
        except ValueError:
            pass
        if value is not None:
            self.setFloat(value, LINE_BIN)

    @Slot(str)
    def floatChangeHex(self, text: str):
        if len(text) != 11:
            return None
        value = None
        try:
            value = hex_str_to_ctypes(text, c_float)
        except ValueError:
            pass
        if value is not None:
            self.setFloat(value, LINE_HEX)

    @Slot(str)
    def doubleChange(self, text: str):
        value = None
        try:
            value = c_double(float(text))
        except ValueError:
            pass
        if value is not None:
            self.setDouble(value, LINE_VALUE)

    @Slot(str)
    def doubleChangeBin(self, text: str):
        if len(text) != 71:
            return None
        value = None
        try:
            value = bin_str_to_ctypes(text, c_double)
        except ValueError:
            pass
        if value is not None:
            self.setDouble(value, LINE_BIN)

    @Slot(str)
    def doubleChangeHex(self, text: str):
        if len(text) != 23:
            return None
        value = None
        try:
            value = hex_str_to_ctypes(text, c_double)
        except ValueError:
            pass
        if value is not None:
            self.setDouble(value, LINE_HEX)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
