import io
import os
from lcd_driver import LCDDriver

class LCDImage(object):

    def __init__(self, lcd_driver: LCDDriver):
        self._driver: LCDDriver = lcd_driver
        self.width = self._driver.width
        self.height = self._driver.height
        self.x = 0
        self.y = 0


    def display_rgb565_binary_file(self, file_path: str):
        try:
            with open(file_path, mode="rb") as f:
                self._driver.set_window(self.x, self.y, self.width, self.height, f.read())

        except OSError as os_ex:
            print(os_ex)
        except Exception as ex:
            print(ex)        

