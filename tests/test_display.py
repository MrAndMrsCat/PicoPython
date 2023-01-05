import time
import os
os.chdir('..')

from LCD.rp_spi_display_interface import RPSPIDisplayInterface
from LCD.lcd_driver import LCDDriver
from LCD.lcd_text import LCDTextWriter
from LCD.lcd_image import LCDImage

interface = RPSPIDisplayInterface()
driver = LCDDriver(interface)

driver.initialize()

sleep = 2

# fill black
driver.clear_screen()

# fill gradient
r, g, b = 0, 0, 0
for x in range(0, 320, 5):
    for y in range(0, 240, 8):
        g = int(255 * x / 320)
        b = int(255 * y / 240)
        pixel = driver.pixel_from_rgb(r, g, b)
        driver.fill_frame_buffer(x, y, 5, 8, pixel)

time.sleep(sleep)

# write some lines of text
driver.clear_screen()
text_writer = LCDTextWriter(driver)
text_writer.console_write_line("Hello world! This is a test of the text writing function")

text_writer.forecolor = 255, 0, 0
lyric = "Mamaaa, Just killed a man, Put a gun against his head, pulled my trigger, Now he's dead" 
text_writer.console_write_line(lyric)

text_writer.forecolor = 0, 0, 255
lyric = "Mamaaa, life had just begun, But now I've gone and thrown it all away"
text_writer.console_write_line(lyric)

text_writer.forecolor = 255, 0, 255
lyric = "Mama, oooh, Didn't mean to make you cry, If I'm not back again this time tomorrow, Carry on, carry on as if nothing really matters"
text_writer.console_write_line(lyric)

time.sleep(sleep)

# write text with changing color
driver.clear_screen()
text_writer.x = 0
text_writer.y = 0
for i in range(37, 255):
    text_writer.forecolor = 0, i, 1
    text_writer.console_write(f"{i} ")

time.sleep(sleep)

# draw an image
image = LCDImage(driver)
image.display_rgb565_binary_file("test_open_fire.rgb565")

