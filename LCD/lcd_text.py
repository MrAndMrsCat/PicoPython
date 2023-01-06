import io
import os
from .lcd_driver import LCDDriver

class LCDTextWriter(object):
    """Displays text on an RGB565 display, either with 'console' behavior, or to specific coordinates"""

    CHAR_WIDTH = 7
    CHAR_HEIGHT = 13
    LINE_FEED = chr(10)
    CARRIAGE_RETURN = chr(13)
    character_bitmaps: dict = None # one font at at time for now, all printable ASCII chars uses 8.6kB

    def __init__(self, lcd_driver: LCDDriver):
        self._driver: LCDDriver = lcd_driver
        self.console_width = int(self._driver.width / self.CHAR_WIDTH)
        self.console_height = int(self._driver.height / self.CHAR_HEIGHT)
        self.x = 0
        self.y = 0
        self.forecolor = 0, 255, 0
        self.backcolor = 0, 0, 0

        if self.character_bitmaps is None:
            self._import_character_bitmaps("./LCD/font/consolas")


    def console_write(self, string: str):
        """Display a string, wrap to a new line if the length exceeds the screen width"""
        for char in string:
            if char == self.CARRIAGE_RETURN: # assume windows line end format (CR + LF), ignore
                continue

            if char == self.LINE_FEED:
                self.console_new_line()
                
            else:
                self.console_write_at(char, self.x, self.y)

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
            self.y = 0 #wrap to top?


    def console_write_at(self, char: chr, x, y):
        """Display a character at this console position"""
        self._set_frame_buffer(char, x * self.CHAR_WIDTH, y * self.CHAR_HEIGHT)


    def write_at(self, string: str, x, y):
        """Display a string at this display coordinate"""
        x_offset = x
        for char in string:
            self._set_frame_buffer(char, x_offset, y)
            x_offset += self.CHAR_WIDTH


    def _set_frame_buffer(self, char: chr, x, y):
        data = self._get_character_bytes(char, self.forecolor, self.backcolor)
        self._driver.set_frame_buffer(x, y, self.CHAR_WIDTH, self.CHAR_HEIGHT, data)
        

    def _get_character_bytes(self, char: chr, forecolor: int, backcolor: int):
        pixels = io.BytesIO(b'')
        for alpha_byte in self.character_bitmaps[char]:
            alpha = alpha_byte / 255.0
            alpha_inv = 1 - alpha
            r1, g1, b1 = forecolor
            r2, g2, b2 = backcolor
            r = int(r1 * alpha + r2 * alpha_inv)
            g = int(g1 * alpha + g2 * alpha_inv)
            b = int(b1 * alpha + b2 * alpha_inv)
            pixels.write(self._driver.pixel_from_rgb(r, g, b))
        return pixels.getvalue()


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

