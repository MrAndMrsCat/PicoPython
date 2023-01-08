import io

class LCDDriver(object):
    """Implements the SPI communication protocol for the ST7789VW LCD controller
    (Waveshare 2inch LCD Module - https://www.waveshare.com/wiki/2inch_LCD_Module)
    """

    # Memory Data Access Control (frame orientation) flags
    MADCTL_MY = 128 # Page Address Order - Bottom to top
    MADCTL_MX = 64  # Column Address Order - Right to Left
    MADCTL_MV = 32  # Page/Column Order - Reverse
    MADCTL_ML = 16  # Line Address Order - LCD Refresh Bottom to Top
    MADCTL_RGB = 8  # RGB/BGR Order
    MADCTL_MH = 4   # Display Data Latch Data Order - LCD Refresh Right to Left 

    def __init__(self, spi_interface):
        self._interface = spi_interface
        self.width = 320
        self.height = 240
        self.max_buffer_length = 4096


    def send_command(self, command: bytes):
        self._interface.send_command(command)


    def send_data(self, data: bytes):
        self._interface.send_data(data)
        self._previous_bytes = data


    def copy_data(self):
        """Send the last bytes again"""
        self._interface.send_data(self._previous_bytes)


    def set_frame_buffer_boundary(self, x: int, y: int, width: int, height: int):
        """Setup the bounderies for the LCD to recieve pixels data"""
        self.send_command(b'\x2A')
        self.send_data(x.to_bytes(2, 'big')) 
        self.send_data((x + width - 1).to_bytes(2, 'big')) 

        self.send_command(b'\x2B')
        self.send_data(y.to_bytes(2, 'big')) 
        self.send_data((y + height - 1).to_bytes(2, 'big')) 

        self.send_command(b'\x2C')


    def fill_frame_buffer(self, x: int, y: int, width: int, height: int, pixel: bytes):
        """Set all pixels to the same value"""
        
        self.set_frame_buffer_boundary(x, y, width, height)
        #for p in range(width * height):
        #    self.send_data(pixel);
            
        self._row_bytes = pixel * width
        for i in range(height):
            self.send_data(self._row_bytes)
            
        #self.send_data(pixel * (width * height))


    def pixel_from_color(self, color: tuple[int, int, int]):
        return self.pixel_from_rgb(*color)
    
            
    def pixel_from_rgb(self, red: int, green: int, blue: int):
        """Convert RGB888 to RGB565"""
        return (
            (int(red & 0b11111000) << 8) | 
            (int(green & 0b11111100) << 3) | 
            (int(blue >> 3) )
            ).to_bytes(2, 'big')


    def pixel_from_mixture(self, forecolor: int, backcolor: int, alpha: int):
        a = alpha / 255.0
        a_inv = 1 - a
        r1, g1, b1 = forecolor
        r2, g2, b2 = backcolor
        r = int(r1 * a + r2 * a_inv)
        g = int(g1 * a + g2 * a_inv)
        b = int(b1 * a + b2 * a_inv)
        return self.pixel_from_rgb(r, g, b)
        

    def fill_all_pixels(self, pixel: bytes):
        """Fill the screen with the same pixel"""
        self.fill_frame_buffer(0, 0, self.width, self.height, pixel)


    def clear_screen(self):
        """Fill the screen black"""
        self.fill_all_pixels(b'\x00\x00')


    def initialize(self):
        self._interface.reset()

        # Memory Data Access Control (orientation essentially) + self.MADCTL_RGB
        self.send_command(b'\x36')
        self.send_data((self.MADCTL_MX + self.MADCTL_MV + self.MADCTL_MH ).to_bytes(1, 'big')) 

        # Interface Pixel Format
        self.send_command(b'\x3A') 
        self.send_data(b'\x05')

        # Display Inversion On
        self.send_command(b'\x21')

        # Column Address Set
        self.send_command(b'\x2A')
        self.send_data(b'\x00\x00\x01\x3F')

        # Row Address Set
        self.send_command(b'\x2B')
        self.send_data(b'\x00\x00\x00\xEF')

        # Porch Setting
        self.send_command(b'\xB2')
        self.send_data(b'\x0C\x0C\x00\x33\x33')

        # Gate Control
        self.send_command(b'\xB7')
        self.send_data(b'\x35') 

        # VCOM Setting
        self.send_command(b'\xBB')
        self.send_data(b'\x1F')

        # LCM Control
        self.send_command(b'\xC0')
        self.send_data(b'\x2C')

        # VDV and VRH Command Enable .
        self.send_command(b'\xC2')
        self.send_data(b'\x01')

        # VRH Set 
        self.send_command(b'\xC3')
        self.send_data(b'\x12')   

        # VDV Set
        self.send_command(b'\xC4')
        self.send_data(b'\x20')

        # Frame Rate Control in Normal Mode
        self.send_command(b'\xC6')
        self.send_data(b'\x0F') 

        # Power Control 1
        self.send_command(b'\xD0')
        self.send_data(b'\xA4\xA1')

        # Positive Voltage Gamma Control
        self.send_command(b'\xE0')
        self.send_data(b'\xD0\x08\x11\x08\x0C\x15\x39\x33\x50\x36\x13\x14\x29\x2D')

        # Negative Voltage Gamma Control
        self.send_command(b'\xE1')
        self.send_data( b'\xD0\x08\x10\x08\x06\x06\x39\x44\x51\x0B\x16\x14\x2F\x31')

        # Display Inversion On
        # Sleep Out
        # Display On 
        self.send_command(b'\x21\x11\x29')