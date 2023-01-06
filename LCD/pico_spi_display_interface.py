#import uasyncio as asyncio
from machine import SPI, Pin, PWM
import time

class PICOSPIDisplayInterface(object):
    """Implements the SPI interface (for the ST7789VW LCD controller) on the Raspberry Pi Pico"""

    # NA - Rx
    # 17 - CSn (CS)
    # 18 - SCK (CLK)
    # 19 - Tx (DIN)
    # 20 - DC
    # 21 - RST
    # 22 - BL (PWM)
    def __init__(self, peripheral=0, baud=40000000, data_command_pin=20, reset_pin=21, backlight_pwm_pin=22):
        self._spi = SPI(peripheral, baudrate=baud, sck=Pin(18), mosi=Pin(19), miso=Pin(16), polarity=1, phase=0)  
        self._backlight_pwm_pin = PWM(Pin(backlight_pwm_pin))
        self._backlight_pwm_pin.freq(1000)
        self._data_command_pin = Pin(data_command_pin, Pin.OUT)
        self._reset_pin = Pin(reset_pin, Pin.OUT)
        self._chip_select_pin = Pin(17, Pin.OUT)
        self.reset()

    def send_command(self, command: bytes):
        self._data_command_pin.off() 
        self._spi.write(command)    

    def send_data(self, data: bytes):
        self._data_command_pin.on() 
        self._spi.write(data)    

    def reset(self):
        self._reset_pin.off()
        time.sleep(0.01)
        self._reset_pin.on()
        time.sleep(0.01)
        self.set_backlight(1)
        self._chip_select_pin.off()

    def set_backlight(self, level: float):
        if (level < 0 or level > 1):
            raise Exception(f"argument level: '{level}' out of range, cannot be <0 or >1")
        else:
            self._backlight_pwm_pin.duty_u16(int(level*65535))
