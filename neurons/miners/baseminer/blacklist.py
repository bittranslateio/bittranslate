# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 Opentensor Foundation

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

# source: https://github.com/opentensor/text-prompting/blob/main/prompting/baseminer/blacklist.py

from typing import Union, Tuple
from neurons.protocol import Translate
import time

request_counts = {}


def call_blacklist( synapse: Translate, config, metagraph, bt) -> Union[Tuple[bool, str], bool]:
    # Check if the key is white listed.
    if synapse.dendrite.hotkey in config.miner.blacklist.whitelist:
        return False, "whitelisted hotkey"

    # Check if the key is black listed.
    if synapse.dendrite.hotkey in config.miner.blacklist.blacklist:
        return True, "blacklisted hotkey"

    if synapse.dendrite.hotkey not in metagraph.hotkeys:
            # Ignore requests from unrecognized entities.
            bt.logging.trace(f'Blacklisting unrecognized hotkey {synapse.dendrite.hotkey}')
            return True, "Unrecognized hotkey"

    # Check registration if we do not allow non-registered users
    if (
        not config.miner.blacklist.allow_non_registered
        and metagraph is not None
        and synapse.dendrite.hotkey not in metagraph.hotkeys
    ):
        return True, "hotkey not registered"

    uid = metagraph.hotkeys.index(synapse.dendrite.hotkey)

    # Check if the key has validator permit
    if config.miner.blacklist.force_validator_permit:
        if synapse.dendrite.hotkey in metagraph.hotkeys:
            if not metagraph.validator_permit[uid]:
                return True, "validator permit required"
        else:
            return True, "validator permit required, but hotkey not registered"

    stake = metagraph.S[uid].item()
    if stake < config.miner.blacklist.minimum_stake_requirement:
        return True, "pubkey stake below min_allowed_stake"

    # blacklist if  too many request
    time_window = 60

    current_time = time.time()
    if synapse.dendrite.hotkey in request_counts:
        requests, start_time = request_counts[synapse.dendrite.hotkey]

        if current_time - start_time > time_window:
            request_counts[synapse.dendrite.hotkey] = (1, current_time)
        elif requests < config.miner.blacklist.max_requests_per_min:
            request_counts[synapse.dendrite.hotkey] = (requests + 1, start_time)
        else:
            bt.logging.info(f"Rate limit exceeded for key: {synapse.dendrite.hotkey}")
            return True, "Rate limited exceeded."
    else:
        request_counts[synapse.dendrite.hotkey] = (1, current_time)


    bt.logging.trace(f'Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}')
    return False, "Hotkey recognized!"