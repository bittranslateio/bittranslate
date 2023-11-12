""" Self-query the miner from a validator's perspective
    to assert that no weird synapse/hashing errors are raised. """

import asyncio
import time

import bittensor
import anyio

from neurons.miners.m2m_miner import M2MMiner
from neurons.protocol import Translate
from mock.mock_network import mocked_network
from mock.mock_blacklist import disable_blacklist_and_verify

async def main():
    # Create dendrite before anything else just in case 
    # there are wallet errors or something similar.
    dendrite = bittensor.dendrite()

    with mocked_network(), disable_blacklist_and_verify():
        miner = M2MMiner()

        miner.axon.start()
        await anyio.sleep(3.0)
        print("English to Polish")
        for idx in range(5):
            synapse = await dendrite.call(
                target_axon=miner.axon,
                synapse=Translate(
                    source_texts=["How's the weather over there?", "It's hot and sunny."],
                    source_lang="en",
                    target_lang="pl"
                ),
                timeout=60.0
            )
            print(f"== SYNAPSE {idx} ==")
            print(f"{synapse=}")
            print(f"{synapse.dendrite.process_time=}")
            print("==TRANSLATION==")
            print(synapse.translated_texts)
            print()

        print("Polish to English ")

        for idx in range(5):
            synapse = await dendrite.call(
                target_axon=miner.axon,
                synapse=Translate(
                    source_texts=["Jaka jest tam pogoda?", "Jest gorąco i słonecznie."],
                    source_lang="pl",
                    target_lang="en"
                ),
                timeout=60.0
            )
            print(f"== SYNAPSE {idx} ==")
            print(f"{synapse=}")
            print(f"{synapse.dendrite.process_time=}")
            print("==TRANSLATION==")
            print(synapse.translated_texts)
            print()

if __name__ == "__main__":
    asyncio.run(main())