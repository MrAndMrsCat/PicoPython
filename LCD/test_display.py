import time

from rp_spi_display_interface import RPSPIDisplayInterface
from lcd_driver import LCDDriver

interface = RPSPIDisplayInterface()
driver = LCDDriver(interface)

driver.initialize()

steps = 3
wait = 1.0

for r in range(0, steps):
    for g in range(0, steps):
        for b in range(0, steps):
            driver.fill_pixels(float(r/steps),float(g/steps),float(b/steps))
            interface.set_backlight((float(r/steps) + float(g/steps) + float(b/steps))/3)
            time.sleep(wait)