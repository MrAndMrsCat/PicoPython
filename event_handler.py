class EventHandler(object):
    def __init__(self):
        self._callbacks: list = []

    def add(self, callback):
        self._callbacks.append(callback)

    def remove(self, callback):
        self._callbacks.remove(callback)

    def invoke(self, sender, args):
        for callback in self._callbacks:
            callback(sender, args)
