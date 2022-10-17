import sys
from ctypes import POINTER, c_char_p, c_double, c_float, cast, sizeof
from typing import TypeVar, Union

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from ui_float import Ui_MainWindow

_T = TypeVar('_T')


def cast_bytes(data_bytes: bytes, ctype: type[_T]) -> _T:
    """Cast bytes to a ctype"""
    assert len(data_bytes) >= sizeof(ctype)
    return cast(
        c_char_p(data_bytes),
        POINTER(ctype)
    ).contents


def bin_str_to_hex(data: str) -> str:
    """Convert a binary string to a hex string"""
    return ''.join(
        f'{int(part, 2):02x}'
        for part in data.split('-')[::-1]
    )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.lineFloat.setText('0.0')
        self._ui.lineDouble.setText('0.0')

    def setBlock(self, block: bool):
        self._ui.lineFloat.blockSignals(block)
        self._ui.lineDouble.blockSignals(block)
        self._ui.lineFloatBin.blockSignals(block)
        self._ui.lineDoubleBin.blockSignals(block)
        self._ui.lineFloatHex.blockSignals(block)
        self._ui.lineDoubleHex.blockSignals(block)

    def setFloat(self, value: Union[c_float, float], event_type: int = 0):
        self.setBlock(True)
        if isinstance(value, float):
            value = c_float(value)
        view = memoryview(value)
        view_bytes = view.tobytes()[::-1]
        bin_text = ''.join(f'{b:08b}' for b in view_bytes)
        if event_type != 0:
            self._ui.lineFloat.setText(str(value.value))
        if event_type != 1:
            self._ui.lineFloatBin.setText(bin_text)
        if event_type != 2:
            self._ui.lineFloatHex.setText(view_bytes.hex())
        self._ui.lcdFloatSign.display(bin_text[0])
        self._ui.lcdFloatExponent.display(bin_text[1:9])
        self._ui.lcdFloatMantissa.display(bin_text[9:])
        self.setBlock(False)

    def setDouble(self, value: Union[c_float, float], event_type: int = 0):
        self.setBlock(True)
        if isinstance(value, float):
            value = c_double(value)
        view = memoryview(value)
        view_bytes = view.tobytes()[::-1]
        bin_text = ''.join(f'{b:08b}' for b in view_bytes)
        if event_type != 0:
            self._ui.lineDouble.setText(str(value.value))
        if event_type != 1:
            self._ui.lineDoubleBin.setText(bin_text)
        if event_type != 2:
            self._ui.lineDoubleHex.setText(view_bytes.hex())
        self._ui.lcdDoubleSign.display(bin_text[0])
        self._ui.lcdDoubleExponent.display(bin_text[1:12])
        self._ui.lcdDoubleMantissa.display(bin_text[12:])
        self.setBlock(False)

    @Slot(str)
    def floatChange(self, text: str):
        value = None
        try:
            value = float(text)
        except ValueError:
            pass
        if value is not None:
            self.setFloat(value, 0)

    @Slot(str)
    def floatChangeBin(self, text: str):
        if len(text) != 35:
            return None
        value = None
        try:
            value = cast_bytes(bytes.fromhex(
                bin_str_to_hex(text)
            ), c_float)
        except KeyboardInterrupt:
            pass
        if value is not None:
            self.setFloat(value, 1)

    @Slot(str)
    def floatChangeHex(self, text: str):
        if len(text) != 11:
            return None
        value = None
        try:
            value = cast_bytes(bytes.fromhex(
                ''.join(text.split('-')[::-1])
            ), c_float)
        except KeyboardInterrupt:
            pass
        if value is not None:
            self.setFloat(value, 2)

    @Slot(str)
    def doubleChange(self, text: str):
        value = None
        try:
            value = float(text)
        except ValueError:
            pass
        if value is not None:
            self.setDouble(value, 0)

    @Slot(str)
    def doubleChangeBin(self, text: str):
        if len(text) != 71:
            return None
        value = None
        try:
            value = cast_bytes(bytes.fromhex(
                bin_str_to_hex(text)
            ), c_double)
        except ValueError:
            pass
        if value is not None:
            self.setDouble(value, 1)

    @Slot(str)
    def doubleChangeHex(self, text: str):
        if len(text) != 23:
            return None
        value = None
        try:
            value = cast_bytes(bytes.fromhex(
                ''.join(text.split('-')[::-1])
            ), c_double)
        except ValueError:
            pass
        if value is not None:
            self.setDouble(value, 2)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
