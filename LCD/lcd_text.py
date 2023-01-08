import io
import os
import math
from .lcd_driver import LCDDriver

class LCDTextWriter(object):
    """Displays text on an RGB565 display, either with 'console' behavior, or to specific coordinates"""

    FONT_BITMAPS_PATH = "./LCD/font/consolas"
    CHAR_WIDTH = 15
    CHAR_HEIGHT = 25
    CONSOLE_CHAR_WIDTH = math.ceil(CHAR_WIDTH / 2)
    CONSOLE_CHAR_HEIGHT = math.ceil(CHAR_HEIGHT / 2)
    LINE_FEED = chr(10)
    CARRIAGE_RETURN = chr(13)
    character_bitmaps: dict = None # one font at at time for now

    # singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LCDTextWriter, cls).__new__(cls)
            cls.x = 0
            cls.y = 0
            cls.forecolor = 0, 255, 0
            cls.backcolor = 0, 0, 0
        return cls._instance


    def initialize(self, lcd_driver: LCDDriver):
        self._driver: LCDDriver = lcd_driver
        self._import_character_bitmaps(self.FONT_BITMAPS_PATH)
        self._frame_buffer = io.BytesIO(b'')
        self.console_width = int(self._driver.width / self.CONSOLE_CHAR_WIDTH)
        self.console_height = int(self._driver.height / self.CONSOLE_CHAR_HEIGHT)


    def console_write(self, string: str):
        """Display a string, wrap to a new line if the length exceeds the screen width"""
        for char in string:
            if char == self.CARRIAGE_RETURN: # assume windows line end format (CR + LF), ignore
                continue

            if char == self.LINE_FEED:
                self.console_new_line()
                
            else:
                self.console_write_at(self.x, self.y, char)

                self.x += 1
                if self.x >= self.console_width:
                    self.console_new_line()


    def console_write_line(self, characters: str):
        """Display a string, then set the console position one row below and reset x (LF + CR)"""
        self.console_write(characters)
        self.console_new_line()


    def console_new_line(self):
        """Set the console position one row below and reset x (LF + CR)"""
        self.x = 0
        self.y += 1
        if self.y >= self.console_height:
            self.y = 0 #wrap to top


    def console_write_at(self, x: int, y: int, char: chr):
        """Display a character at this console position"""
        self.write_character_at(char, x * self.CONSOLE_CHAR_WIDTH, y * self.CONSOLE_CHAR_HEIGHT, "half")


    def write_at(self, x: int, y: int, string: str, scale: str = "full"):
        """Display a string at this display coordinate"""
        x_offset = x
        x_increment = self.CHAR_WIDTH if scale == "full" else self.CONSOLE_CHAR_WIDTH
        for char in string:
            self.write_character_at(char, x_offset, y, scale)
            x_offset += x_increment


    def write_character_at(self, char: chr, x: int, y: int, scale: str = "full"):
        if scale == "full":
            self._driver.set_frame_buffer_boundary(x, y, self.CHAR_WIDTH, self.CHAR_HEIGHT)
            read_offset = 1
            #buffer_size = self.CHAR_WIDTH * self.CHAR_HEIGHT
        else:
            self._driver.set_frame_buffer_boundary(x, y, self.CONSOLE_CHAR_WIDTH, self.CONSOLE_CHAR_HEIGHT)
            read_offset = 2
            #buffer_size = self.CONSOLE_CHAR_WIDTH * self.CONSOLE_CHAR_HEIGHT

        alpha_bitmap = self.character_bitmaps[char]

        for y in range(0, self.CHAR_HEIGHT, read_offset):
            for x in range(0, self.CHAR_WIDTH, read_offset):
                pixel = self._driver.pixel_from_mixture(self.forecolor, self.backcolor, alpha_bitmap[x + y * self.CHAR_WIDTH])
                #self._driver.send_data(pixel)
                self._frame_buffer.write(pixel)

            self._driver.send_data(self._frame_buffer.getvalue())
            self._frame_buffer.seek(0)


    def _get_character_bytes(self, char: chr, forecolor: int, backcolor: int, scale: int = 1):
        pixels = io.BytesIO(b'')
        if scale == 1:
            for alpha_byte in self.character_bitmaps[char]:
                pixels.write(self._driver.pixel_from_mixture(forecolor, backcolor, alpha_byte))
        else:
            row = io.BytesIO(b'')
            index = 0
            bitmap = self.character_bitmaps[char]
            for y in range(self.CHAR_HEIGHT):
                for x in range(self.CHAR_WIDTH):
                    alpha_byte = bitmap[index]
                    row.write(self._driver.pixel_from_mixture(forecolor, backcolor, alpha_byte) * scale)
                    index += 1
                for r in range(scale):
                    pixels.write(row.getvalue())
                row.seek(0)


    def _import_character_bitmaps(self, directory: str):
        self.character_bitmaps = {}
        try:
            # filename is ASCII character code (decimal).bin
            for file_path in os.listdir(directory):
                char = chr(int(file_path.split('.')[0]))
                with open(f"{directory}/{file_path}", mode="rb") as f:
                    self.character_bitmaps[char] = f.read()

        except OSError as os_ex:
            print(os_ex)
        except Exception as ex:
            print(ex)        

