from machine import Pin
from event_timer import EventTimer

class OnboardLED(object):

    def __init__(self):
        self._led = Pin("LED", Pin.OUT, value=0)
        self._flash_timer = EventTimer(100)
        self._flash_timer.elapsed.add(self._flash_timer_elapsed)
        self._flash_timer.name = "led flash"
        self._toggle_count = -1
        self.off()


    def on(self):
        self._flash_timer.stop()
        self._last_steady_state = "on"
        self._led.on()


    def off(self):
        self._flash_timer.stop()
        self._last_steady_state = "off"
        self._led.off()


    def value(self, enabled: bool):
        if enabled:
            self.on()
        else:
            self.off()


    def flash(self, count: int = 1, interval_ms: float = 100):
        self._toggle_count = count * 2
        self._flash_timer.interval_ms = interval_ms
        self._flash_timer.start()


    def _flash_timer_elapsed(self, sender, args):
        if self._toggle_count > 0:
            self._toggle_count -= 1
            self._led.toggle()  

        elif self._toggle_count == 0:
            self._toggle_count -= 1
            if self._last_steady_state == "on":
                self.on()
            else:
                self.off()
