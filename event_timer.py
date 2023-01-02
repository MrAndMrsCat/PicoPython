import time
import uasyncio as asyncio
from event_handler import EventHandler

class EventTimer(object):

    def __init__(self, interval_ms: float, enabled = False):
        self.elapsed: EventHandler = EventHandler()
        self.interval_ms: float = interval_ms
        self._enabled: bool = enabled
        self._task = None
        self._reset_time = None
        self.name = "unknown"


    async def _loop(self):
        try:
            sleep_ms = self.interval_ms
            while self._enabled:
                call_time = time.ticks_ms()
                await asyncio.sleep_ms(sleep_ms)

                if not self._enabled:
                    break

                if self._reset_time is not None:
                    sleep_ms = self._reset_time + self.interval_ms - time.ticks_ms()
                    self._reset_time = None
                    continue

                self.elapsed.invoke(self, None)

                elapsed_time = time.ticks_ms() - call_time
                sleep_ms = self.interval_ms - (elapsed_time - self.interval_ms)
                sleep_ms = min(self.interval_ms, sleep_ms)
        finally:
            self._task = None


    def start(self):
        if not self._enabled:
            self._enabled = True
            self._task = asyncio.create_task(self._loop())


    def stop(self):
        self._enabled = False
        try:
            if self._task is not None:
                self._task.cancel()
        except Exception as ex:
            pass


    def enabled(self, enable: bool):
        if enable:
            self.start()
        else:
            self.stop()


    def reset(self):
        if not self._enabled:
            self.start()
        else:
            self._reset_time = time.ticks_ms()