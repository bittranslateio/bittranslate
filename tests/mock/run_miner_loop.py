""" Script to run the miner loop with components mocked out.
    Demonstrates that the metagraph-syncing calls and 
    weight-setting calls occur at the rate we expect,
    with the parameters we expect. """

import time
from typing import Iterator
from contextlib import contextmanager, ExitStack
from unittest.mock import patch, seal, PropertyMock

import bittensor
import torch

from neurons.miners.m2m_miner import M2MMiner
from mock.mock_network import mocked_network

TIME_SCALE = 1e-3 # Run simulation way faster to observe results quickly.

@contextmanager
def log_subtensor_block() -> Iterator[None]:
    """ Patch the `subtensor.block` attribute to log, 
        and increase at a regular rate. """
    
    t_start = time.monotonic()

    def get_block(*args,**kwargs) -> int:
        # Assuming 12 second blocks, increment the block time every 12 seconds.
        # Start at 1.
        # Assume that it takes some time to query current block.
        time.sleep(2.0 * TIME_SCALE)
        block = int((time.monotonic()-t_start)/12/TIME_SCALE)+1
        bittensor.logging.info(f"subtensor.block = {block}")
        return block

    with patch.object(
        bittensor.subtensor,
        'block',
        new_callable=PropertyMock
    ) as mock:
        mock.side_effect = get_block
        seal(mock)
        yield

@contextmanager
def log_set_weights() -> Iterator[None]:
    """ Patch the `subtensor.set_weights()` attribute to log. """

    def set_weights(self,*args,**kwargs) -> bool:
        bittensor.logging.info(
            f"set_weights("
            f"args={repr(args)}, "
            f"kwargs={repr(kwargs)}"
            f")"
        )

    with patch.object(
        bittensor.subtensor,
        'set_weights',
        set_weights
    ) as mock:
        yield
        
@contextmanager
def mock_metagraph_sync_get_block() -> Iterator[None]:
    """ Mock the `bittensor.metagraph.sync()` method
        to only fetch the subtensor block. """
    
    def sync(self, *args, **kwargs) -> None:
        bittensor.logging.info("metagraph.sync()")
        self.block = torch.nn.Parameter(
            torch.tensor(
                [kwargs["subtensor"].block], 
                dtype=torch.int64
            ), 
            requires_grad=False
        )

    with patch.object(bittensor.metagraph, 'sync', sync) as mock:
        yield None

@contextmanager
def mock_subtensor_subnetwork_n() -> Iterator[None]:
    with patch.object(bittensor.subtensor, 'subnetwork_n') as mock:
        # Pretend there are 12 peers 
        # so we can easily identify the 1 amongst the 0s.
        mock.return_value = 12 
        seal(mock)
        yield

def main():
    with ExitStack() as exit_stack:
        exit_stack.enter_context(mocked_network())
        exit_stack.enter_context(log_subtensor_block())
        exit_stack.enter_context(log_set_weights())
        exit_stack.enter_context(mock_metagraph_sync_get_block())
        exit_stack.enter_context(mock_subtensor_subnetwork_n())

        miner = M2MMiner()
        miner.run()

if __name__ == "__main__":
    main()