# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# source: https://github.com/opentensor/bittensor-subnet-template/blob/main/neurons/miner.py

import typing
import traceback
import argparse

import bittensor as bt
from neurons.protocol import Translate
from abc import abstractmethod
from neurons.miners.baseminer.blacklist import call_blacklist
from neurons.miners.baseminer.config import get_config
from neurons.miners.baseminer.priority import call_priority

from .verify_data import verify_synapse_data

class BaseMiner:

    def __init__(self):
        parser = argparse.ArgumentParser(description="")
        # Adds args from child class
        self.add_args(parser)

        self.config = get_config(parser)

        # Activating Bittensor's logging with the set configurations.
        bt.logging(config=self.config, logging_dir=self.config.full_path)
        bt.logging.info(
            f"Running miner for subnet: {self.config.netuid} on network: {self.config.subtensor.chain_endpoint} with config:")

        # This logs the active configuration to the specified logging directory for review.
        bt.logging.info(self.config)

        # Step 4: Initialize Bittensor miner objects
        # These classes are vital to interact and function within the Bittensor network.
        bt.logging.info("Setting up bittensor objects.")

        # Wallet holds cryptographic information, ensuring secure transactions and communication.
        self.wallet = bt.wallet(config=self.config)
        bt.logging.info(f"Wallet: {self.wallet}")

        # subtensor manages the blockchain connection, facilitating interaction with the Bittensor blockchain.
        self.subtensor = bt.subtensor(config=self.config)
        bt.logging.info(f"Subtensor: {self.subtensor}")

        # metagraph provides the network's current state, holding state about other participants in a subnet.
        self.metagraph = self.subtensor.metagraph(self.config.netuid)
        bt.logging.info(f"Metagraph: {self.metagraph}")

        if self.wallet.hotkey.ss58_address not in self.metagraph.hotkeys:
            bt.logging.error(
                f"\nYour miner: {self.wallet} is not registered to chain connection: {self.subtensor} \nRun btcli register and try again. ")
            exit()

        # Each miner gets a unique identity (UID) in the network for differentiation.
        # NOTE: This is quite the misnomer. Speaking explicitly, 
        # this is the UID of a miner within a particular subnet.
        self.my_subnet_uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)
        bt.logging.info(f"Running miner on uid: {self.my_subnet_uid}")

        # Step 6: Build and link miner functions to the axon.
        # The axon handles request processing, allowing validators to send this process requests.
        self.axon = bt.axon(wallet=self.wallet, config=self.config)
        bt.logging.info(f"Axon {self.axon}")

        # Attach determiners which functions are called when servicing a request.
        bt.logging.info(f"Attaching forward function to axon.")
        self.axon.attach(
            forward_fn=self.forward,
            blacklist_fn=self.blacklist_fn,
            priority_fn=self.priority_fn,
        )

    # Step 5: Set up miner functionalities
    # The following functions control the miner's response to incoming requests.
    # The blacklist function decides if a request should be ignored.
    def blacklist_fn(self, synapse: Translate) -> typing.Tuple[bool, str]:
        return call_blacklist(synapse, self.config, self.metagraph, bt)



    # The priority function determines the order in which requests are handled.
    # More valuable or higher-priority requests are processed before others.
    def priority_fn(self, synapse: Translate) -> float:
        # Miners may recieve messages from multiple entities at once. This function
        # determines which request should be processed first. Higher values indicate
        # that the request should be processed first. Lower values indicate that the
        # request should be processed later.
        # Below: simple logic, prioritize requests from entities with more stake.
        caller_uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)  # Get the caller index.
        priority = float(self.metagraph.S[caller_uid])  # Return the stake as the priority.
        call_priority(synapse, self.config, self.metagraph)
        bt.logging.trace(f'Prioritizing {synapse.dendrite.hotkey} with value: ', priority)
        return priority


    def run(self):
        axon = self.axon # alias

        # Serve passes the axon information to the network + netuid we are hosting on.
        # This will auto-update if the axon port of external ip have changed.
        bt.logging.info(
            f"Serving axon on network: {self.config.subtensor.chain_endpoint} with netuid: {self.config.netuid}")
        axon.serve(netuid=self.config.netuid, subtensor=self.subtensor)

        # Start  starts the miner's axon, making it active on the network.
        bt.logging.info(f"Starting axon server on port: {self.config.axon.port}")
        axon.start()

        bt.logging.info(f"Querying for the current block")
        # Step 7: Keep the miner alive
        # This loop maintains the miner's operations until intentionally stopped.
        bt.logging.info(f"Starting main loop")
        step = 0
        last_updated_block = self.subtensor.block

        while True:
            try:
                # Below: Periodically update our knowledge of the network graph.
                current_block = self.subtensor.block

                blocks_per_sync = 10
                if current_block - self.metagraph.block >= blocks_per_sync:
                    self.metagraph.sync( subtensor = self.subtensor )
                    self.my_subnet_uid = self.metagraph.hotkeys.index(
                        self.wallet.hotkey.ss58_address
                    )
                    log = (
                        f'Step:{step} | '
                        f'Block:{self.metagraph.block.item()} | '
                        f'Stake:{self.metagraph.S[self.my_subnet_uid]} | '
                        f'Rank:{self.metagraph.R[self.my_subnet_uid]} | '
                        f'Trust:{self.metagraph.T[self.my_subnet_uid]} | '
                        f'Consensus:{self.metagraph.C[self.my_subnet_uid]} | '
                        f'Incentive:{self.metagraph.I[self.my_subnet_uid]} | '
                        f'Emission:{self.metagraph.E[self.my_subnet_uid]}'
                    )
                    bt.logging.info(log)

                step += 1
                # Sleep is not necessary here 
                # because syncing the metagraph
                # will space out the time anyways.
                #time.sleep(1)

            # If someone intentionally stops the miner, it'll safely terminate operations.
            except KeyboardInterrupt:
                axon.stop()
                bt.logging.success('Miner killed by keyboard interrupt.')
                break
            # In case of unforeseen errors, the miner will log the error and continue operations.
            except Exception as e:
                bt.logging.error(traceback.format_exc())
                continue


    @abstractmethod
    def forward(self, synapse: Translate) -> Translate:
        pass

    @abstractmethod
    def add_args(self, synapse: argparse.ArgumentParser):
        pass

    def verify_synapse_data(self, synapse: Translate) -> None:
        verify_synapse_data(self, synapse)