import time

from LCD.lcd_driver import LCDDriver
from LCD.lcd_text import LCDTextWriter
from LCD.lcd_image import LCDImage
from LCD.lcd_drawing import LCDDrawing
#from micrologger import MicroLogger

pico = False

if pico:
    from LCD.pico_spi_display_interface import PICOSPIDisplayInterface
    interface = PICOSPIDisplayInterface()
else:
    from LCD.rp_spi_display_interface import RPSPIDisplayInterface
    interface = RPSPIDisplayInterface()

#MicroLogger.level = MicroLogger.DEBUG
#logger = MicroLogger("TestDisplayMain")

driver = LCDDriver(interface)
#drawing = LCDDrawing(driver)

drawing = LCDDrawing()
drawing.initialize(driver)


#logger.debug("initialize()")
driver.initialize()

# fill black
#logger.debug("clear_screen()")
driver.clear_screen()

drawing.rectangle_filled(0, 319, 0, 239, (255, 0, 64))

for i in range(10, 120, 20):
    drawing.rectangle(0 + i, 319 - i, 0 + i, 239 - i, 10, (i, 0, 0))

drawing.circle_filled(160, 120, 110, (200, 0, 200))

text = LCDTextWriter()
text.initialize(driver)

text.console_write_line("Hello world! This is a test of the text writing function")

from LCD.ui_indicator import Indicator

controls = []
indicator1 = Indicator(x=90, y=55, shape="rectangle", text="WiFi connected")
controls.append(indicator1)

indicator2 = Indicator(x=90, y=70, shape="circle", text="Automation connected")
controls.append(indicator2)

indicator3 = Indicator(x=90, y=85, shape="circle", text="Initialized")
controls.append(indicator3)

indicator4 = Indicator(x=90, y=100, shape="circle", text="Boiler Enabled")
controls.append(indicator4)

for control in controls:
    control.draw()

time.sleep(2)

for control in controls:
    control.enable(True)

time.sleep(2)

for control in controls:
    control.enable(False)