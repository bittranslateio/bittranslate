from typing import Optional
from time import perf_counter

class Timer:
    """ Context manager that tracks elapsed time spent in block. """

    _start: Optional[float] = None
    """ Start time in seconds, computed via `time.perf_counter()` """

    _end: Optional[float] = None
    """ End time in seconds, computed via `time.perf_counter()` """

    def elapsed_seconds(self) -> float:
        """ How many seconds did this timer capture? """
        if self._start and self._end:
            return self._end - self._start
        else:
            raise ValueError("Cannot measure incomplete timer")

    def __enter__(self):
        self._start = perf_counter()
        return self

    def __exit__(self,*args):
        self._end = perf_counter()