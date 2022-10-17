import sys
from ctypes import c_double, c_float, sizeof
from typing import TypeVar

LITTLEENDIAN = True
BYTE_SELICE = slice(None, None, -1)


_T = TypeVar('_T')


class MyAssertionError(Exception):
    pass


def my_assert(condition: bool, desc: str = None) -> None:
    """ for `__debug__ == False`, `assert` will be ignored. """
    if not condition:
        raise MyAssertionError(desc)


def check_system():
    global LITTLEENDIAN, BYTE_SELICE
    # check for little endian
    if sys.byteorder == 'little':
        LITTLEENDIAN = True
    else:
        LITTLEENDIAN = False
    if not LITTLEENDIAN:
        BYTE_SELICE = slice(None)
    # check for 32 / 64 bit
    my_assert(sizeof(c_float) == 4, 'sizeof(c_float) != 4')
    my_assert(sizeof(c_double) == 8, 'sizeof(c_double) != 8')
    # TODO: check for IEEE 754
    # Maybe is not necessary, 100% sure that all modern CPUs are IEEE 754 compliant


def cast_bytes_to_ctypes(data_bytes: bytes, ctype: type[_T]) -> _T:
    """Cast bytes to a ctype"""
    my_assert(
        len(data_bytes) >= sizeof(ctype),
        'len(data_bytes) < sizeof(ctype)'
    )
    # return cast(
    #     c_char_p(data_bytes),
    #     POINTER(ctype)
    # ).contents
    return ctype.from_buffer_copy(data_bytes)


def bin_str_to_hex(data: str) -> str:
    """Convert a binary string to a hex string"""
    return ''.join(
        f'{int(part, 2):02x}'
        for part in data.split('-')[BYTE_SELICE]
    )


def hex_str_to_ctypes(text: str, ctype: type[_T]) -> _T:
    """Convert a hex string to a binary string"""
    return cast_bytes_to_ctypes(
        bytes.fromhex(
            ''.join(text.split('-')[BYTE_SELICE])
        ),
        ctype
    )


def bin_str_to_ctypes(data: str, ctype: type[_T]) -> _T:
    """Convert a binary string to a ctypes value"""
    return cast_bytes_to_ctypes(
        bytes.fromhex(
            bin_str_to_hex(data)
        ),
        ctype
    )


def ctypes_to_str(ctype_data) -> tuple[str, str]:
    """Convert a ctypes value to a binary string"""
    view = memoryview(ctype_data)
    view_bytes = view.tobytes()[BYTE_SELICE]
    return (
        ''.join(f'{b:08b}' for b in view_bytes),
        view_bytes.hex()
    )
