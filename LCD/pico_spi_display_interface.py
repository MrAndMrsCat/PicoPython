#import uasyncio as asyncio
from machine import SPI, Pin, PWM
import time

class PICOSPIDisplayInterface(object):
    # NA - Rx
    # 17 - CSn
    # 18 - SCK
    # 19 - Tx
    # 20 - DC
    # 21 - RST
    # 22 - BL (PWM)
    def __init__(self, peripheral=0, baud=40000000, data_command_pin=20, reset_pin=21, backlight_pwm_pin=22):
        self._spi = SPI(peripheral, baudrate=baud)  
        self._backlight_pwm_pin = PWM(Pin(backlight_pwm_pin))
        self._backlight_pwm_pin.freq(1000)
        self._data_command_pin = Pin(data_command_pin)
        self._reset_pin = Pin(reset_pin)
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

    def set_backlight(self, level: float):
        if (level < 0 or level > 1):
            raise Exception(f"argument level: '{level}' out of range, cannot be <0 or >1")
        else:
            self._backlight_pwm_pin.duty(int(level*1023))