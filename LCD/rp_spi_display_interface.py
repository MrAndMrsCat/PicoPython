import RPi.GPIO as GPIO
import spidev
import time

class RPSPIDisplayInterface(object):
    """Implements the SPI interface (for the ST7789VW LCD controller) on the Raspberry Pi 4B"""

    # NA - Rx
    # 24 - CSn
    # 23 - SCK
    # 19 - DIN (Tx)
    # 22 - DC
    # 13 - RST
    # 12 - BL (PWM)

    SPI_BUFFER_LEN = 4096

    def __init__(self, peripheral=0, baud=40000000, data_command_pin=25, reset_pin=27, backlight_pwm_pin=18):
        self._spi = spidev.SpiDev(0,peripheral)
        self._spi.max_speed_hz = baud
        self._spi.mode = 0b00
        self._reset_pin= reset_pin
        self._data_command_pin = data_command_pin
        self._backlight_pwm_pin = backlight_pwm_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._reset_pin, GPIO.OUT)
        GPIO.setup(self._data_command_pin, GPIO.OUT)
        GPIO.setup(self._backlight_pwm_pin, GPIO.OUT)    
        self._backlight_pwm=GPIO.PWM(self._backlight_pwm_pin, 1000)
        self._backlight_pwm.start(100)

        self.reset()

    def send_command(self, command: bytes):
        GPIO.output(self._data_command_pin, GPIO.LOW)
        self._spi.writebytes(command) 

    def send_data(self, data: bytes):
        GPIO.output(self._data_command_pin, GPIO.HIGH)
        
        for i in range(0, len(data), self.SPI_BUFFER_LEN):
            self._spi.writebytes(data[i:i+self.SPI_BUFFER_LEN])   

    def reset(self):
        GPIO.output(self._reset_pin, 0)
        time.sleep(0.01)
        GPIO.output(self._reset_pin, 1)
        time.sleep(0.01)
        self.set_backlight(1)

    def set_backlight(self, level: float):
        if (level < 0 or level > 1):
            raise Exception(f"argument level: '{level}' out of range, cannot be <0 or >1")
        else:
            # print(f"set_baclight(level={level:.2f})")
            self._backlight_pwm.ChangeDutyCycle(level*100)