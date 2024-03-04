from contextlib import contextmanager
from typing import Iterator
from unittest.mock import patch, seal

import neurons.miners.baseminer.baseminer as miner_module
from neurons.miners.baseminer.baseminer import BaseMiner
from neurons.protocol import Translate
from substrateinterface.base import Keypair

@contextmanager
def disable_blacklist() -> Iterator[None]:
    with patch.object(miner_module, 'call_blacklist') as mock:
        mock.return_value = False,""
        seal(mock)
        yield

@contextmanager
def disable_verify() -> Iterator[None]:
    with patch.object(Keypair, 'verify') as mock:
        mock.return_value = True
        seal(mock)
        yield None

def priority(self, synapse: Translate) -> float:
    return 0.0

@contextmanager
def disable_priority() -> Iterator[None]:
    with patch.object(BaseMiner, 'priority_fn', priority) as mock:
        yield

@contextmanager
def disable_blacklist_and_verify() -> Iterator[None]:
    with disable_blacklist(), disable_verify(), disable_priority():
        yield None