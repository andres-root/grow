"""Code timing for profiling."""

import time


class Timer(object):
    """Times code to see how long it takes using a context manager."""

    def __init__(self, key, label=None, meta=None):
        self._time = time
        self.key = key
        self.label = label or key
        self.meta = meta
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = self._time.time()
        return self

    def __exit__(self, *args):
        self.end = self._time.time()

    def __repr__(self):
        if self.label != self.key:
            return '<Timer:{} {} : {}>'.format(self.key, self.label, self.duration)
        return '<Timer:{} : {}>'.format(self.key, self.duration)

    @property
    def duration(self):
        """Duration of timer."""
        return self.end - self.start

    def export(self):
        """Export the timer data."""
        return {
            'key': self.key,
            'meta': self.meta,
            'start': self.start,
            'end': self.end,
        }


class Profile(object):
    """Keeps track of all of the timer usage."""

    def __init__(self):
        self.timers = []

    def __iter__(self):
        for timer in self.timers:
            yield timer

    def timer(self, *args, **kwargs):
        """Create a new timer."""
        timer = Timer(*args, **kwargs)
        self.timers.append(timer)
        return timer

    def export(self):
        """Export the timer data for each timer created."""
        return [t.export() for t in self.timers]
