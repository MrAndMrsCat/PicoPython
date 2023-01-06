import math
from .lcd_driver import LCDDriver

class LCDDrawing(object):
    """Draw simple shapes"""

    # singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LCDDrawing, cls).__new__(cls)
            # Remove __init__() and put any initialization here.
        return cls._instance


    def initialize(self, lcd_driver: LCDDriver):
        self._driver: LCDDriver = lcd_driver


    def rectangle_filled(self, x_start: int, x_end: int, y_start: int, y_end: int, color: tuple[int, int, int]):
        """Draw a filled rectangle"""
        r, g, b = color
        pixel = self._driver.pixel_from_rgb(r,g,b)
        width = x_end - x_start
        height = y_end - y_start
        self._driver.fill_frame_buffer(x_start, y_start, width, height, pixel)


    def rectangle(self, x_start: int, x_end: int, y_start: int, y_end: int, weight: int, color: tuple[int, int, int]):
        """Draw a rectangle outline with a line weight"""
        if x_end - x_start > weight and y_end - y_start > weight:
            # top
            self.rectangle_filled(x_start, x_end, y_start, x_start + weight, color)
            # bottom
            self.rectangle_filled(x_start, x_end, y_end - weight, y_end, color)
            # left
            self.rectangle_filled(x_start, x_start + weight, y_start + weight, y_end - weight, color)
            # right
            self.rectangle_filled(x_end - weight, x_end, y_start + weight, y_end - weight, color)
        else:
            raise Exception("Invalid rectangle parameters")

    def circle_filled(self, x: int, y: int, radius: int, color: tuple[int, int, int]):
        if x - radius >= 0 and y - radius >= 0:
            r, g, b = color
            pixel = self._driver.pixel_from_rgb(r,g,b)
            y_top = y
            y_top_prev = x

            for x_left in range(0, radius): 
                # Pythagoras
                adjacent = radius - x_left
                y_top = int(math.sqrt(radius * radius - adjacent * adjacent))

                stripe_height = y_top - y_top_prev

                if stripe_height > 0:
                    stripe_width = (radius - x_left) * 2 # extend to semi-circle
                    x_start = x - radius + x_left
                    # top 
                    self._driver.fill_frame_buffer(x_start, y - y_top, stripe_width, stripe_height, pixel)
                    # bottom 
                    self._driver.fill_frame_buffer(x_start, y + y_top - stripe_height, stripe_width, stripe_height, pixel)
                y_top_prev = y_top

        else:
            raise Exception(f"Invalid circle parameters x={x}, y={y}, radius={radius}")
