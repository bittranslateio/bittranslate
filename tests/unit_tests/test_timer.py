import time

import pytest

from bittranslate.timer import Timer

EPSILON = 1e-2
SLEEP_SECONDS = 1e-2

@pytest.mark.lite
def test_timer():
    with Timer() as timer:
        time.sleep(SLEEP_SECONDS)

    assert abs(timer.elapsed_seconds()-SLEEP_SECONDS) < EPSILON

    with Timer() as timer:
        time.sleep(2*SLEEP_SECONDS)

    assert abs(timer.elapsed_seconds()-2*SLEEP_SECONDS) < EPSILON