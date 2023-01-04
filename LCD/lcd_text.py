import io
import os
from lcd_driver import LCDDriver

class LCDTextWriter(object):
    CHAR_WIDTH = 7
    CHAR_HEIGHT = 13
    character_bitmaps = {}

    def __init__(self, lcd_driver: LCDDriver):
        self._driver: LCDDriver = lcd_driver
        self.console_width = int(self._driver.width / self.CHAR_WIDTH)
        self.console_height = int(self._driver.height / self.CHAR_HEIGHT)
        self.console_pos = 0, 0
        self.forecolor = 0.0, 1.0, 0.0
        self.backcolor = 0.0, 0.0, 0.0
        self._import_character_bitmaps("./font/consolas")


    def console_write(self, characters: str):
        x, y = self.console_pos
        for char in characters:
            self.console_write_at(char, x, y)

            x += 1
            if x >= self.console_width:
                x = 0
                y += 1
                if y >= self.console_width:
                    y = 0 #wrap to top?
        
        self.console_pos = x, y 


    def console_write_at(self, character, x, y):
        self.write_at(character, x * self.CHAR_WIDTH, y * self.CHAR_HEIGHT)


    def write_at(self, character, x, y):
        data = self._get_character_bytes(character, self.forecolor, self.backcolor)
        self._driver.set_window(x, y, self.CHAR_WIDTH, self.CHAR_HEIGHT, data)
        

    def _get_character_bytes(self, character, forecolor, backcolor):
        pixels = io.BytesIO(b'')
        for alpha_byte in self.character_bitmaps[character]:
            alpha = alpha_byte / 255
            alpha_comp = 1 - alpha
            r1, g1, b1 = forecolor
            r2, g2, b2 = backcolor
            r = r1 * alpha + r2 * alpha_comp
            g = g1 * alpha + g2 * alpha_comp
            b = b1 * alpha + b2 * alpha_comp
            pixels.write(self._driver.pixel_from_rgb(r, g, b))
        return pixels.getvalue()


    def _import_character_bitmaps(self, directory: str):
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

