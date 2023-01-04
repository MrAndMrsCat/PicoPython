import time

from rp_spi_display_interface import RPSPIDisplayInterface
from lcd_driver import LCDDriver
from lcd_text import LCDTextWriter

interface = RPSPIDisplayInterface()
driver = LCDDriver(interface)

driver.initialize()
driver.clear()


#r, g, b, count = 0.0, 0.0, 0.0, 0
#for x in range(0, 240, 8):
#    for y in range(0, 320, 16):
#        r = x / 240.0
#        b = y / 320.0
#        count += 1
#        pixel = driver.pixel_from_rgb(r, g, b)
#        driver.fill_window(x, y, 8, 16, pixel)


text_writer = LCDTextWriter(driver)
text_writer.console_write("Hello world! This is a test of the text writing function")

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