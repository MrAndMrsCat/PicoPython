import time

from LCD.pico_spi_display_interface import PICOSPIDisplayInterface
from LCD.lcd_driver import LCDDriver
from LCD.lcd_text import LCDTextWriter
from LCD.lcd_image import LCDImage
from micrologger import MicroLogger
from microdiagnostics import MicroDiagnostics

MicroLogger.level = MicroLogger.DEBUG
logger = MicroLogger("TestDisplayMain")


interface = PICOSPIDisplayInterface()
driver = LCDDriver(interface)

logger.debug("initialize()")
driver.initialize()

sleep = 2

# fill black
logger.debug("clear_screen()")
driver.clear_screen()

#logger.debug("fill gradient")
## fill gradient
#r, g, b = 0, 0, 0
#for x in range(0, 320, 5):
#    for y in range(0, 240, 8):
#        g = int(255 * x / 320)
#        b = int(255 * y / 240)
#        pixel = driver.pixel_from_rgb(r, g, b)
#        driver.fill_frame_buffer(x, y, 5, 8, pixel)

#time.sleep(sleep)

# write some lines of text
logger.debug("clear_screen()")
driver.clear_screen()
text_writer = LCDTextWriter(driver)
logger.debug("console_write_line()")
text_writer.console_write_line("Hello world! This is a test of the text writing function")

text_writer.forecolor = 255, 0, 0
lyric = "Mamaaa, Just killed a man, Put a gun against his head, pulled my trigger, Now he's dead"
logger.debug("console_write_line()")
text_writer.console_write_line(lyric)

text_writer.forecolor = 0, 0, 255
lyric = "Mamaaa, life had just begun, But now I've gone and thrown it all away"
logger.debug("console_write_line()")
text_writer.console_write_line(lyric)

text_writer.forecolor = 255, 0, 255
lyric = "Mama, oooh, Didn't mean to make you cry, If I'm not back again this time tomorrow, Carry on, carry on as if nothing really matters"
logger.debug("console_write_line()")
text_writer.console_write_line(lyric)

#time.sleep(sleep)

# write text with changing color
logger.debug("clear_screen()")
driver.clear_screen()
logger.debug("console_write() * 218")
text_writer.x = 0
text_writer.y = 0
for i in range(37, 255):
    text_writer.forecolor = 0, i, 1
    logger.verb("console_write()")
    text_writer.console_write(f"{i} ")

#time.sleep(sleep)

# draw an image
image = LCDImage(driver)
logger.debug("display_rgb565_binary_file()")
image.display_rgb565_binary_file("test_open_fire.rgb565")


