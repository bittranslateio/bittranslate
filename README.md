# BitTranslate
BitTranslate is a Subnet that rewards high-quality translations. 
Validators produce unique text using a multilingual text generation model. 
The text is then sent to Miners which apply a text-to-text model to produce a translation. 
The validator then evaluates the outputted translations using two Reward Models that are based on the methods from academic papers.

The subnet has been designed to be able to accommodate numerous translation pairs. 
The initial subnet supports pairs of languages including English, German, Spanish, Italian, and Polish. 
We have plans to soon support many other languages. 
![BitTranslate Logo](https://www.bittranslate.io/wp-content/themes/lucrosus-child/assets/images/logos/logo_bitttranslate.svg)

## Installation
```bash
git clone https://github.com/bittranslateio/bittranslate.git
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

#### Exams 
Paper: [EXAMS: A Multi-subject High School Examinations Dataset for Cross-lingual and Multilingual Question Answering](https://aclanthology.org/2020.emnlp-main.438.pdf)
Hugging Face: [exams](https://huggingface.co/datasets/exams)
Used for: Italian and Polish 

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

Used for: English, German and  Spanish  


## Mining 
```bash
python3 neurons/miners/m2m_miner.py --netuid 2 --axon.port 70000 --logging.debug --wallet.name default --wallet.hotkey default 
```
 Parameters

| Parameter                                 | Default                | Description                                                                                   |
|-------------------------------------------|------------------------|-----------------------------------------------------------------------------------------------|
| device                                    | "cuda"                 | What device to use for the model.                                                             | 
| max_batch_size                            | 2                      | The maximum allowed batch size (number of source texts) for an incoming request               |
| max_char                                  | 512                    | Maximum allowed characters for source text.                                                   |
| max_length                                | 128                    | The token length that source text will be truncated to                                        |
| model_name                                | "facebook/m2m100_1.2B" | Either a Hugging Face ID or a path to a local path that contains both the model and tokenizer |
| miner.blacklist.whitelist                 | []                     | Whitelisted keys                                                                              |
| miner.blacklist.blacklist                 | []                     | Blacklisted keys                                                                              |
| miner.blacklist.force_validator_permit    | False                  | If True, requests not from validators  will be blacklisted                                    |
| miner.blacklist.allow_non_registered      | False                  | If True, allow non-registered hotkeys to mine                                                 |
| miner.blacklist.minimum_stake_requirement | 1024                   | Minimum stake required for a hotkey to avoid being blacklisted                                |

## Validating  
```bash
python3 neurons/validator.py --netuid 2 --axon.port 70000 --logging.debug --wallet.name default --wallet.hotkey default 
```
 Parameters: 

| Parameter           | Default             | Description                                                                                                                                                                        |
|---------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| device              | "cuda"              | "cuda" if detected else "cpu"                                                                                                                                                      |
| max_char            | 512                 | Maximum allowed characters for translated text.                                                                                                                                    |
| batch_size          | 2                   | The number of source texts that are sent to the miners every request. Miners by default ignore request with more than 2 source texts, so we do not recommend increasing this value |
| miners_per_step     | 8                   | The number of miners to query in each step                                                                                                                                         |
| save_tracking_steps | 100                 | Number of steps before tracked scores and texts are saved.                                                                                                                         |
| miners_per_step     | "bittranslate_out/" | Output directory for tracked results.                                                                                                                                              |
