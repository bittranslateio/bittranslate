# ⛏️ Mining Docs

## Installation
```bash
git clone https://github.com/LucrosusCapital/bittranslate.git
cd bittranslate
pip install -e . 
```

Bittensor must be installed separately.  

```bash
pip install bittensor
```

## Usage

To start mining on the Bittranslate subnetwork you need to create your coldkey, hotkey, and register it on netuid 2.

Creating Coldkey
```bash
btcli w new_coldkey
```
Creating Hotkey
```bash
btcli w new_hotkey
```
Registering your Hotkey
```bash
btcli s register --netuid 2 --wallet.name YOUR_COLDKEY --wallet.hotkey YOUR_HOTKEY
```
Now you are ready to start mining!
```bash
python3 neurons/miners/m2m_miner.py --netuid 2  --axon.port  70000 --logging.debug
```

Parameters 

| Parameter                                 | Default                | Description                                                                                                    |
|-------------------------------------------|------------------------|----------------------------------------------------------------------------------------------------------------|
| device                                    | "cuda"                 | The device to use for the model.                                                                               |
| max_batch_size                            | 2                      | The maximum allowed batch size (number of source texts) for an incoming request.                               |
| max_char                                  | 1024                   | Maximum allowed characters for source text.                                                                    |
| max_length                                | 1024                   | The token length that source text will be truncated to.                                                        |
| model_name                                | "facebook/m2m100_1.2B" | Either a Hugging Face ID or a path to a local path that contains both the model and tokenizer.                 |
| tracking_file                             | "bittranslate.json"    | File to output source texts and translated texts to, in JSON format                                            |
| miner.blacklist.whitelist                 | []                     | Whitelisted keys                                                                                               |
| miner.blacklist.blacklist                 | []                     | Blacklisted keys                                                                                               |
| miner.blacklist.force_validator_permit    | False                  | If True, requests not from validators  will be blacklisted                                                     |
| miner.blacklist.allow_non_registered      | False                  | If True, allow non-registered hotkeys to mine                                                                  |
| miner.blacklist.minimum_stake_requirement | 1024                   | Minimum stake required for a hotkey to avoid being blacklisted                                                 |
| miner.blacklist.max_requests_per_min      | 4                      | The maximum allowed requests a validator can send to a miner per minute before getting blacklisted.            |
| disable_set_weight                        | False                  | If true, weights will not be updated. Can be used to run a miner in addition to a validator from the same key. |
| do_sample                                 | False                  | If true, sampling is used.                                                                                     |
| top_k                                     | 10                     | Number of highest probability words to consider for each generation (when do_sample is True).                  |
| temperature                               | 1.0                    | How likely low-probability tokens are to be selected (if do_sample is True).                                   |
| num_beams                                 | 1                      | Number of beams for beam search. Default is  1`, meaning no beam search.                                       |
| no_repeat_ngram_size                      | 0                      | Prevents n-grams of the given value from repeating                                                             |
