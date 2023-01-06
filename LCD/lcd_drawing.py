from .lcd_driver import LCDDriver

class LCDDrawing(object):
    """Draw simple shapes"""

    ## singleton
    #_instance = None
    #def __new__(cls):
    #    if cls._instance is None:
    #        cls._instance = super(LCDDrawing, cls).__new__(cls)
    #        # Remove __init__() and put any initialization here.
    #    return cls._instance

    def __init__(self, lcd_driver: LCDDriver):
        self._driver: LCDDriver = lcd_driver

    def line_orthogonal(self, x: int, y: int, weight: int):

        pass

    def rectangle(self, x: int, y: int, width: int, height: int, weight: int):

        pass


