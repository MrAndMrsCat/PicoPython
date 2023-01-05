import time

from rp_spi_display_interface import RPSPIDisplayInterface
from lcd_driver import LCDDriver
from lcd_text import LCDTextWriter
from lcd_image import LCDImage

interface = RPSPIDisplayInterface()
driver = LCDDriver(interface)

driver.initialize()
driver.clear()

#r, g, b = 0.0, 0.0, 0.0
#for x in range(0, 320, 8):
#    for y in range(0, 240, 16):
#        r = x / 320.0
#        b = y / 240.0
#        pixel = driver.pixel_from_rgb(r, g, b)
#        driver.fill_window(x, y, 8, 16, pixel)
#        time.sleep(0.05)

driver.clear()
text_writer = LCDTextWriter(driver)
text_writer.console_write_line("Hello world! This is a test of the text writing function")

text_writer.forecolor = 1, 0, 0
lyric = "Mamaaa, Just killed a man, Put a gun against his head, pulled my trigger, Now he's dead" 
text_writer.console_write_line(lyric)

text_writer.forecolor = 0, 0, 1
lyric = "Mamaaa, life had just begun, But now I've gone and thrown it all away"
text_writer.console_write_line(lyric)

text_writer.forecolor = 1, 0, 1
lyric = "Mama, oooh, Didn't mean to make you cry, If I'm not back again this time tomorrow, Carry on, carry on as if nothing really matters"
text_writer.console_write_line(lyric)


driver.clear()
image = LCDImage(driver)
image.display_rgb565_binary_file("test.rgb565")

#steps = 3
#wait = 0.25

#quad = 0
#for r in range(0, steps):
#    for g in range(0, steps):
#        for b in range(0, steps):
#            x = 0 if quad < 2 else 120
#            y = 0 if quad % 2 == 0 else 160

#            pixel = driver.pixel_from_rgb(float((r+1)/steps),float((g+1)/steps),float((b+1)/steps))

#            driver.fill_window(x, y, 120, 160, pixel)

#            quad = (quad + 1) % 4

#            time.sleep(wait)

#for r in range(0, steps):
#    for g in range(0, steps):
#        for b in range(0, steps):
#            driver.fill_pixels(float((r+1)/steps),float((g+1)/steps),float((b+1)/steps))
#            #interface.set_backlight((float(r/steps) + float(g/steps) + float(b/steps))/3)
#            time.sleep(wait)