from .lcd_text import LCDTextWriter
from .lcd_drawing import LCDDrawing


class Indicator(object):

    _text_writer = LCDTextWriter()
    _drawing = LCDDrawing()

    def __init__(self, x: int, y: int, shape: str = "rectangle", text: str = ""):
        self.x: int = x
        self.y: int = y
        self.shape: str = shape
        self.text: str = text
        self.border: int = 2
        self.size = LCDTextWriter.CHAR_HEIGHT
        self.text_scale: str = "full"
        self.enabled: bool = False
        self.enabled_color = (0, 255, 0)
        self.disabled_color = (100, 100, 100)
        self.back_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        

    def draw(self):
        # background
        self._drawing.rectangle_filled(
            x_start=self.x, 
            y_start=self.y, 
            x_end=self.x + self.size + self.border,  
            y_end=self.y + self.size, 
            color=self.back_color
            )
        self._text_writer.forecolor = self.text_color
        self._text_writer.write_at(self.x + self.size + self.border, self.y, self.text, self.text_scale)
        self.draw_indicator()


    def draw_indicator(self):
        color = self.enabled_color if self.enabled else self.disabled_color
        size = self.size - self.border * 2 

        if self.shape == "rectangle":
            self._drawing.rectangle_filled(
                x_start=self.x + self.border, 
                y_start=self.y + self.border, 
                x_end=self.x + self.border + size,  
                y_end=self.y + self.border + size, 
                color=color)
        else:
            radius = int(size / 2)
            self._drawing.circle_filled(
                x=self.x + self.border + radius, 
                y=self.y + self.border + radius, 
                radius=radius, 
                color=color
                )


    def enable(self, value: bool):
        if value != self.enabled:
            self.enabled = value
            self.draw_indicator()