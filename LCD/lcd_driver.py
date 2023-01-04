import io

class LCDDriver(object):
    def __init__(self, spi_interface):
        self._spi = spi_interface
        self.width = 320
        self.height = 240


    def _command(self, command: bytes):
        self._spi.send_command(command)


    def _data(self, data: bytes):
        self._spi.send_data(data)
  

    def set_window(self, x: int, y: int, width: int, height: int, pixels: bytes):
        self._command(b'\x2A')
        self._data(x.to_bytes(2, 'big')) 
        self._data((x + width - 1).to_bytes(2, 'big')) 

        self._command(b'\x2B')
        self._data(y.to_bytes(2, 'big')) 
        self._data((y + height - 1).to_bytes(2, 'big')) 

        self._command(b'\x2C')
        self._data(pixels)


    def pixel_from_rgb(self, red: float, green: float, blue: float):
        r = int(red * 0b11111)
        g = int(green * 0b111111) << 5
        b = int(blue * 0b11111) << 11
        return (r|g|b).to_bytes(2, 'big')


    def fill_window(self, x: int, y: int, width: int, height: int, pixel: bytes):
        pixels = io.BytesIO(b'')
        for p in range(width * height):
            pixels.write(pixel)
        self.set_window(x, y, width, height, pixels.getvalue())


    def fill_rgb(self, red: float, green: float, blue: float):
        self.fill(self.pixel_from_rgb(red, green, blue))
        

    def fill(self, pixel: bytes):
        self.fill_window(0, 0, self.height, self.width, pixel)


    def clear(self):
        self.fill(b'\x00\x00')


    def initialize(self):
        self._spi.reset()

        self._command(b'\x36')
        self._data(b'\x00') 
        self._command(b'\x3A') 
        self._data(b'\x05')
        self._command(b'\x21\x2A')
        self._data(b'\x00\x00\x01\x3F')
        self._command(b'\x2B')
        self._data(b'\x00\x00\x00\xEF')
        self._command(b'\xB2')
        self._data(b'\x0C\x0C\x00\x33\x33')
        self._command(b'\xB7')
        self._data(b'\x35') 
        self._command(b'\xBB')
        self._data(b'\x1F')
        self._command(b'\xC0')
        self._data(b'\x2C')
        self._command(b'\xC2')
        self._data(b'\x01')
        self._command(b'\xC3')
        self._data(b'\x12')   
        self._command(b'\xC4')
        self._data(b'\x20')
        self._command(b'\xC6')
        self._data(b'\x0F') 
        self._command(b'\xD0')
        self._data(b'\xA4\xA1')
        self._command(b'\xE0')
        self._data(b'\xD0\x08\x11\x08\x0C\x15\x39\x33\x50\x36\x13\x14\x29\x2D')
        self._command(b'\xE1')
        self._data( b'\xD0\x08\x10\x08\x06\x06\x39\x44\x51\x0B\x16\x14\x2F\x31')
        self._command(b'\x21\x11\x29')