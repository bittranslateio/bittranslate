from typing import Iterator, Optional
from contextlib import contextmanager
from dataclasses import dataclass

import bittensor

from .timer import Timer

@dataclass
class BoxedTime:
    """ Object to hold a time. """
    time: Optional[float] = None

@contextmanager
def log_elapsed_time(name: str) -> Iterator[BoxedTime]:
    boxed_time = BoxedTime()
    try:
        with Timer() as timer:
            yield boxed_time
    finally:
        bittensor.logging.info(
            f"Elapsed time ({name}) = "
            f"{timer.elapsed_seconds():.3f} seconds"
        )
        boxed_time.time = timer.elapsed_seconds()