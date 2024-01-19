# BitTranslate
BitTranslate is a Subnet that rewards high-quality translations. Validators produce unique text using a multilingual text generation model. 
The text is then sent to Miners which apply a text-to-text model to produce a translation. 
The validator then evaluates the outputted translations using two Reward Models that are based on the methods from academic papers.

The subnet has been designed to be able to accommodate numerous translation pairs. 

This is the list of currently supported languages:
- Arabic: **"ar"**
- Bulgarian: **"bg"**
- Chinese: **"zh"**
- English: **"en"**
- Estonian: **"et"**
- Finnish: **"fi"**
- French: **"fr"**
- German: **"de"**
- Greek: **"el"**
- Hindi: **"hi"**
- Hungarian: **"hu"**
- Italian: **"it"**
- Korean: **"ko"**
- Persian: **"fa"**
- Polish: **"pl"**
- Portuguese: **"pt"**
- Romanian: **"ro"**
- Russian: **"ru"**
- Spanish: **"es"**
- Swedish: **"sv"**
- Thai: **"th"**
- Turkish: **"tr"**
- Ukrainian: **"uk"**
- Vietnamese: **"vi"**


We have plans to soon support many other languages.
![BitTranslate Logo](https://github.com/bittranslateio/bittranslate/blob/main/bittranslate_logo_white.png)

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
## Technical Overview

### Reward Models
#### BertScore
Based on the paper [BERTSCORE: EVALUATING TEXT GENERATION WITH BERT](https://arxiv.org/pdf/1904.09675.pdf) that uses [BertScore](https://github.com/Tiiiger/bert_score) to evaluate translated text.

#### VectorSim
Inspired by the STransQuest technique from [TransQuest: Translation Quality Estimation with  Cross-lingual Transformers](https://aclanthology.org/2020.coling-main.445.pdf). But, instead of using XLM-RoBERTa we used [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) to compute the similarity of the source and translated texts.

### Datasets 
Validators use text from following datasets as a prompt for a text generation model that produces text which is then sent to miners. 

#### BitTranslate Datasets
We open-sourced datasets for 7 languages to expand the languages available on BitTranslate. 

Hugging Face: [datasets](https://huggingface.co/BitTranslate)

Used for: Estonian, Persian, Finnish, French, Korean, Swedish, Ukrainian


#### Exams 
Paper: [EXAMS: A Multi-subject High School Examinations Dataset for Cross-lingual and Multilingual Question Answering](https://aclanthology.org/2020.emnlp-main.438.pdf)

Hugging Face: [exams](https://huggingface.co/datasets/exams)

Used for: Bulgarian, Chinese, Hungarian, Italian, Polish, Portuguese, Turkish, Vietnamese

#### GermanQuAD
Paper: [GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://aclanthology.org/2021.mrqa-1.4.pdf)

Hugging Face: [deepset/germanquad](https://huggingface.co/datasets/deepset/germanquad)

Used for: German 

#### PeerSum
Paper: [Summarizing Multiple Documents with Conversational Structure for Meta-review Generation](https://arxiv.org/pdf/2305.01498.pdf)

Hugging Face: [oaimli/PeerSum](https://huggingface.co/datasets/oaimli/PeerSum)

Used for: English 

#### xQuAD
Paper: [On the cross-lingual transferability of monolingual representations](https://arxiv.org/pdf/1910.11856.pdf)

Hugging Face: [xquad](https://huggingface.co/datasets/xquad)

Used for: Arabic, Chinese, English, German, Greek, Spanish, Hindi, Romanian, Russian, Thai, Turkish, Vietnamese

#### MKQA
Paper: [MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering](https://arxiv.org/pdf/2007.15207.pdf)

Hugging Face: [mkqa](https://huggingface.co/datasets/mkqa)

Used for: French

### Models
#### mGPT

Paper: [mGPT: Few-Shot Learners Go Multilingual](https://arxiv.org/pdf/2204.07580.pdf)

Hugging Face: [ai-forever/mGPT](https://huggingface.co/ai-forever/mGPT)

Purpose: Validators use this model to generate original text that's sent to miners. 

### Wenzhong-GPT2-110M

Paper:[Fengshenbang 1.0: Being the Foundation of Chinese Cognitive Intelligence](https://arxiv.org/pdf/2209.02970.pdf)

Hugging Face: [IDEA-CCNL/Wenzhong-GPT2-110M](https://huggingface.co/IDEA-CCNL/Wenzhong-GPT2-110M)

Purpose: The same purpose as mGPT, but except exclusively used to produce Chinese text. 

#### M2M

Paper: [Beyond English-Centric Multilingual Machine Translation](https://arxiv.org/pdf/2010.11125.pdf)

Hugging Face: [facebook/m2m100_1.2B](https://huggingface.co/facebook/m2m100_1.2B)

Purpose: The default model miners use to perform translation.   


## Mining 

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

## Validating  
```bash
python3 neurons/validator.py --netuid 2  --axon.port  70000 --logging.debug
```
 Parameters: 

| Parameter          | Default             | Description                                                                                                                                                                          |
|--------------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| device             | "cuda"              | "cuda" if detected else "cpu"                                                                                                                                                        |
| max_char           | 1024                | Maximum allowed characters for translated text.                                                                                                                                      |
| batch_size         | 2                   | The number of source texts that are sent to the miners every request. Miners by default ignore request with more than 2 source texts, so we do not recommend increasing this value   |
| miners_per_step    | 8                   | The number of miners to query in each step                                                                                                                                           |
| track_steps        | 100                 | Number of steps before tracked scores and texts are saved.                                                                                                                           |
| out_dir            | "bittranslate_out/" | Output directory for tracked results.                                                                                                                                                |
| enable_api         | False               | If set, a callable API will be activated.                                                                                                                                            |
| score_api          | False               | If set,  responses from API requests will be used to modify scores.                                                                                                                  |
| api_json           | "neurons/api.json"  | A path to a a config file for the API.                                                                                                                                               |
| no_artificial_eval | False               | If set, artificial data will not be sent to miners for the purpose of scoring. We only recommend setting this to true to when debugging the API.                                     |
| ngrok_domain       | None                | If set, expose the API over ngrok to the specified domain                                                                                                                            |
| update_steps       | 500                 | The number of steps until we check if there has been a new version. If 0, no searching will be performed.                                                                            |
| no_restart         | False               | If set, the process is not restarted when a new version is detected.                                                                                                                 |


## Optional: Validator API
Validators have the can enable a REST API to allow them to produce translates for arbitrary text.  
The API can be enabled by supplying the "--enable_api" parameter. 

### Request Format
```python
import requests
response = requests.post(
        f'http://127.0.0.1:{9999}/translate', # provide the port number you supplied to  "--axon.port"
        headers={"auth": "change-me"}, # place the API key where "change-me" is. 
        json={
            "source_texts": ["hello world"], # you may provide a list of texts. Do not exceed 512 characters per source text or include more than 2 source texts. 
            "source_lang": "auto", # Language code for the source text, or auto for it to be classified automatically.  
            "target_lang":  "es" # Language code for the translated text. 
        }
    )
print(response.json()) 
# {'detail': 'success', 'translated_texts': ['Hola Mundo']}
```

### Config

The validator.py's "--api_json" parameter is for a path to a JSON config that defines API keys along with their rate limits. 
By default, a config file will be loaded from "neurons/api.json" will be loaded. Change the API key ID to a long UUID within this the file before deploying.  
This file can be edited as the validator is running without requiring a restart. 

```json
{
  "keys": {"3f1f582c-a735-4326-8cea-b9f70fda9d78": {"requests_per_min":  4},
          "c0b0c1cd-47df-4c62-8d03-bf7d279daa48": {"requests_per_min":  2}}
}
```
### Scoring 
By default, the responses from miners for API requests are not used to update the scores for the models. This can be enabled by passing the "--score_api" parameter.

### Security 
The API is hosted over HTTP, which is not secure.
To expose the API over a secure (HTTPS) endpoint,
sign up for a premium "ngrok" account and run the `ngrok config add-authtoken ...`
command from the [your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) page.
Then, create a domain from the [domains](page).
We recommend using an "ngrok.app" domain rather than an "ngrok-free.app" domain,
as the later is blocked by some internet providers.

With the setup complete, launch the validator with the NGROK_DOMAIN environment variable, 
as well as 
```sh
python neurons/validator.py <other-args-such-as-wallet> --enable_api --ngrok_domain fluffy-blue.ngrok.app
```

If you instead want to use some other kind of reverse-proxy service, run it in a separate process.

### Debugging 
We recommend using the parameter "--no_artificial_eval" when debugging the API. 
This will disable artificial responses from being generated and sent to miners. 
Thus, simplifying the output logs of the validator. Don't forget to relaunch your validator without the "--no_artificial_eval" as soon as you're done testing. 

You can ping the API with "scripts/ping_api.py". Please refer to its get_config() method to learn about its CLI parameters. 
