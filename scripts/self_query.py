""" Query a running miner to test out 
    the functionality of a specific synapse. """


import argparse
import asyncio
import base64
from pathlib import Path
import os

import bittensor
from io import BytesIO

from neurons.protocol import Translate

PROJECT_ROOT = Path(__file__).parent.parent

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        type=int,
        default=8091
    )

    parser.add_argument(
        "--axon_wallet_name",
        required=True
    )
    parser.add_argument(
        "--axon_hotkey_name",
        default="default"
    )

    return parser.parse_args()


async def query_translate(
        args: argparse.Namespace,
        dendrite: bittensor.dendrite,
        target_axon: bittensor.AxonInfo
):

    synapse: Translate = await dendrite.call(
        target_axon=target_axon,
        synapse=Translate(
            source_texts=["Hello world"],
            source_lang="en",
            target_lang="pl"
        )
    )

    print(synapse)

async def main(args: argparse.Namespace):
    wallet = bittensor.wallet(
        name=args.axon_wallet_name,
        hotkey=args.axon_hotkey_name
    )

    dendrite = bittensor.dendrite()
    target_axon = bittensor.AxonInfo(
        version=3,
        ip='127.0.0.1',
        port=args.port,
        ip_type=4,
        hotkey=wallet.hotkey.ss58_address,
        coldkey=wallet.coldkey.ss58_address
    )

    await query_translate(
        args=args,
        dendrite=dendrite,
        target_axon=target_axon
    )
    

if __name__ == "__main__":
    asyncio.run(main(get_args()))