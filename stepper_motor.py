import uasyncio as asyncio
from machine import Pin
from micrologger import MicroLogger
from event_handler import EventHandler

logger = MicroLogger("StepperMotor")

class StepperMotor(object):
    bit_masks = [0x1, 0x2, 0x4, 0x8]
    drive_patterns = {
        "wave" : [0x1, 0x2, 0x4, 0x8], # seldom used, conserves some power
        "full" : [0x3, 0x6, 0xC, 0x9], # often used, maximizes torque
        "half" : [0x1, 0x3, 0x2, 0x6, 0x4, 0xC, 0x8, 0x9] # maximizes resolution, but has variable torque
        }


    def __init__(self, first_pin: int = 10, drive_pattern: str = "full", steps_per_sec: int = 50):
        logger.verb(f"__init__(first_pin={first_pin}, drive_pattern={drive_pattern}, steps_per_sec={steps_per_sec})")
        self.move_completed: EventHandler = EventHandler()
        self.steps_per_sec: int = steps_per_sec
        self._pins = [Pin(x + first_pin, Pin.OUT) for x in range(4)]
        self._drive_pattern = StepperMotor.drive_patterns[drive_pattern]
        self._position: int = 0


    def set_position(self, position: int):
        bits = self._drive_pattern[position]
        for pin, mask in enumerate(StepperMotor.bit_masks):
            self._pins[pin].value(mask & bits > 0)


    def move(self, direction: str = "right"):
        step = 1 if direction == "right" else -1
        self._position = (self._position + step) % len(self._drive_pattern)
        self.set_position(self._position)
       
        
    def move_steps(self, steps: int, hold: bool = False):
        logger.verb(f"move_steps(steps={steps}, hold={hold})")
        asyncio.create_task(self._move_steps(steps, hold))
    

    async def _move_steps(self, steps, hold):
        try:
            interval = int(1000 / self.steps_per_sec)
            step = 1 if steps > 0 else -1
            for x in range(abs(steps)):
                self._position = (self._position + step) % len(self._drive_pattern)
                self.set_position(self._position)
                await asyncio.sleep_ms(interval)
            if not hold:
                self.deactivate()
            self.move_completed.invoke(self, {"steps" : steps, "hold" : hold})
        except Exception as ex:
            logger.exception(ex)


    def deactivate(self):
        logger.verb("deactivate()")
        for pin in self._pins:
            pin.off()
