from contextlib import contextmanager, ExitStack
from typing import Iterator
from unittest.mock import patch, seal, PropertyMock

from bittensor.metagraph import metagraph
from substrateinterface import SubstrateInterface
import bittensor
from bittensor.mock.wallet_mock import MockWallet
import neurons.miners.baseminer.baseminer as baseminer_module

@contextmanager
def mock_miner_exit() -> Iterator[None]:
    """ Mock the `os.exit()` function for the base miner
        to prevent exit due to missing metagraph hotkey. """
    with patch.object(baseminer_module, 'exit') as mock:
        # Turn `exit()` into a no-op.
        mock.return_value = None
        seal(mock)
        yield None


@contextmanager
def mock_metagraph_sync() -> Iterator[None]:
    """ Mock the `bittensor.metagraph.sync()` method
        to prevent network contact during offline testing. """
    with patch.object(metagraph, 'sync') as mock:
        # Turn `.sync()` into a no-op.
        mock.return_value = None
        seal(mock)
        yield None

@contextmanager
def mock_subtensor_wss_connection() -> Iterator[None]:
    """ Mock the `SubstrateInterface.connect_websocket()` method
        to avoid any connection to the subtensor. """
    with patch.object(SubstrateInterface, 'connect_websocket') as mock:
        # Turn `.connect_websocket()` into a no-op.
        mock.return_value = None
        seal(mock)
        yield None

@contextmanager
def mock_subtensor_reload_type_registry() -> Iterator[None]:
    """ Mock the `SubstrateInterface.reload_type_registry()` method
        to avoid errors from the lack of websocket connection. """
    with patch.object(SubstrateInterface,'reload_type_registry') as mock:
        # Turn `.reload_type_registry()` into a no-op.
        mock.return_value = None
        seal(mock)
        yield None

@contextmanager
def mock_subtensor_serve_axon() -> Iterator[None]:
    with patch.object(bittensor.subtensor, 'serve_axon') as mock:
        mock.return_value = None
        seal(mock)
        yield

@contextmanager
def mock_wallet() -> Iterator[None]:
    with patch.object(bittensor, 'wallet', MockWallet) as mock:
        seal(mock)
        yield None

@contextmanager
def mock_metagraph_has_hotkey(ss58_address: str) -> Iterator[None]:
    with patch.object(
        metagraph, 'hotkeys', 
        new_callable=PropertyMock
    ) as mock:
        mock.return_value = [ss58_address]
        seal(mock)
        yield None

@contextmanager
def mocked_network() -> Iterator[None]:
    with ExitStack() as exit_stack:
        exit_stack.enter_context(mock_miner_exit())
        exit_stack.enter_context(mock_metagraph_sync())
        exit_stack.enter_context(mock_subtensor_wss_connection())
        exit_stack.enter_context(mock_subtensor_reload_type_registry())
        exit_stack.enter_context(mock_wallet())
        exit_stack.enter_context(mock_subtensor_serve_axon())
        exit_stack.enter_context(mock_metagraph_has_hotkey(
            MockWallet().hotkey.ss58_address
        ))

        yield None