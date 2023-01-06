import io

class LCDDriver(object):
    """Implements the SPI communication protocol for the ST7789VW LCD controller
    (Waveshare 2inch LCD Module)
    """

    # Memory Data Access Control (frame orientation) flags
    MADCTL_MY = 128 # Page Address Order - Bottom to top
    MADCTL_MX = 64  # Column Address Order - Right to Left
    MADCTL_MV = 32  # Page/Column Order - Reverse
    MADCTL_ML = 16  # Line Address Order - LCD Refresh Bottom to Top
    MADCTL_RGB = 8  # RGB/BGR Order
    MADCTL_MH = 4   # Display Data Latch Data Order - LCD Refresh Right to Left 

    def __init__(self, spi_interface):
        self._spi = spi_interface
        self.width = 320
        self.height = 240
        self.max_buffer_length = 4096


    def _command(self, command: bytes):
        self._spi.send_command(command)


    def _data(self, data: bytes):
        self._spi.send_data(data)


    def set_frame_buffer(self, x: int, y: int, width: int, height: int, pixels: bytes):
        """Set pixels from left to right, top to bottom"""
        self._command(b'\x2A')
        self._data(x.to_bytes(2, 'big')) 
        self._data((x + width - 1).to_bytes(2, 'big')) 

        self._command(b'\x2B')
        self._data(y.to_bytes(2, 'big')) 
        self._data((y + height - 1).to_bytes(2, 'big')) 

        self._command(b'\x2C')
        self._data(pixels)


    def fill_frame_buffer(self, x: int, y: int, width: int, height: int, pixel: bytes):
        """Set all pixels to the same value"""
        buf = io.BytesIO(b'')
        
        if width * height * 2 > self.max_buffer_length: # conserve memory
            for p in range(width):
                buf.write(pixel)

            for y_idx in range(height):
                self.set_frame_buffer(x, y + y_idx, width, 1, buf.getvalue())

        else:
            for p in range(width * height):
                buf.write(pixel)
            self.set_frame_buffer(x, y, width, height, buf.getvalue())


    def pixel_from_rgb(self, red: int, green: int, blue: int):
        """Convert RGB888 to RGB565"""
        r = int(red & 0b11111000) << 8
        g = int(green & 0b11111100) << 3
        b = int(blue >> 3) 
        return (r|g|b).to_bytes(2, 'big')
        

    def fill_all_pixels(self, pixel: bytes):
        """Fill the screen with the same pixel"""
        self.fill_frame_buffer(0, 0, self.width, self.height, pixel)


    def clear_screen(self):
        """Fill the screen black"""
        self.fill_all_pixels(b'\x00\x00')


    def initialize(self):
        self._spi.reset()

        # Memory Data Access Control (orientation essentially) + self.MADCTL_RGB
        self._command(b'\x36')
        self._data((self.MADCTL_MX + self.MADCTL_MV + self.MADCTL_MH ).to_bytes(1, 'big')) 

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