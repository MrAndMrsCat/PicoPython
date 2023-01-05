import io

class LCDDriver(object):

    #  Memory Data Access Control (frame orientation) flags
    MADCTL_MY = 128   # Page Address Order - Bottom to top
    MADCTL_MX = 64   # Column Address Order - Right to Left
    MADCTL_MV = 32   # Page/Column Order - Reverse
    MADCTL_ML = 16   # Line Address Order - LCD Refresh Bottom to Top
    MADCTL_RGB = 8 # RGB/BGR Order
    MADCTL_MH = 4  # Display Data Latch Data Order - LCD Refresh Right to Left 

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
        self.fill_window(0, 0, self.width, self.height, pixel)


    def clear(self):
        self.fill(b'\x00\x00')


    def initialize(self):
        self._spi.reset()

        # Memory Data Access Control (orientation essentially)
        self._command(b'\x36')
        self._data((self.MADCTL_MX + self.MADCTL_MV + self.MADCTL_MH).to_bytes(1, 'big')) 

        # Interface Pixel Format
        self._command(b'\x3A') 
        self._data(b'\x05')

        # Display Inversion On
        self._command(b'\x21')

        # Column Address Set
        self._command(b'\x2A')
        self._data(b'\x00\x00\x01\x3F')

        # Row Address Set
        self._command(b'\x2B')
        self._data(b'\x00\x00\x00\xEF')

        # Porch Setting
        self._command(b'\xB2')
        self._data(b'\x0C\x0C\x00\x33\x33')

        # Gate Control
        self._command(b'\xB7')
        self._data(b'\x35') 

        # VCOM Setting
        self._command(b'\xBB')
        self._data(b'\x1F')

        # LCM Control
        self._command(b'\xC0')
        self._data(b'\x2C')

        # VDV and VRH Command Enable .
        self._command(b'\xC2')
        self._data(b'\x01')

        # VRH Set 
        self._command(b'\xC3')
        self._data(b'\x12')   

        # VDV Set
        self._command(b'\xC4')
        self._data(b'\x20')

        # Frame Rate Control in Normal Mode
        self._command(b'\xC6')
        self._data(b'\x0F') 

        # Power Control 1
        self._command(b'\xD0')
        self._data(b'\xA4\xA1')

        # Positive Voltage Gamma Control
        self._command(b'\xE0')
        self._data(b'\xD0\x08\x11\x08\x0C\x15\x39\x33\x50\x36\x13\x14\x29\x2D')

        # Negative Voltage Gamma Control
        self._command(b'\xE1')
        self._data( b'\xD0\x08\x10\x08\x06\x06\x39\x44\x51\x0B\x16\x14\x2F\x31')

        # Display Inversion On
        # Sleep Out
        # Display On 
        self._command(b'\x21\x11\x29')