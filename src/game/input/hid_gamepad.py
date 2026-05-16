import ctypes
import ctypes.util

# Report layout for vendor 0x0583 / product 0x2060:
#   byte 0 = X axis  (0–255, center 128)
#   byte 1 = Y axis  (0–255, center 128)
#   byte 2 = buttons bitmask (bit 0 = btn 1 … bit 7 = btn 8)
VENDOR  = 0x0583
PRODUCT = 0x2060
AXIS_DEAD_ZONE = 40


def _load_hidapi():
    lib = ctypes.util.find_library('hidapi')
    if lib:
        try:
            return ctypes.CDLL(lib)
        except OSError:
            pass
    for path in ('/opt/homebrew/lib/libhidapi.dylib', '/usr/local/lib/libhidapi.dylib'):
        try:
            return ctypes.CDLL(path)
        except OSError:
            continue
    return None


class HidGamepad:
    def __init__(self, vendor=VENDOR, product=PRODUCT):
        lib = _load_hidapi()
        if lib is None:
            raise OSError('hidapi not found')
        lib.hid_open.restype  = ctypes.c_void_p
        lib.hid_open.argtypes = [ctypes.c_ushort, ctypes.c_ushort, ctypes.c_wchar_p]
        lib.hid_read.restype  = ctypes.c_int
        lib.hid_read.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
        lib.hid_set_nonblocking.restype  = ctypes.c_int
        lib.hid_set_nonblocking.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.hid_close.restype  = None
        lib.hid_close.argtypes = [ctypes.c_void_p]
        self._lib = lib
        self._dev = lib.hid_open(vendor, product, None)
        if not self._dev:
            raise OSError('hid_open failed')
        lib.hid_set_nonblocking(self._dev, 1)

    def read(self):
        """Return the latest HID report as a list of ints, or None if no data."""
        buf = ctypes.create_string_buffer(8)
        latest = None
        while True:
            n = self._lib.hid_read(self._dev, buf, 8)
            if n <= 0:
                break
            latest = list(buf.raw[:n])
        return latest

    def close(self):
        if self._dev:
            self._lib.hid_close(self._dev)
            self._dev = None
