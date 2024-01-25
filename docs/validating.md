# 🧑‍🏫 Validating

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
| no_restart         | False               | If set, the process is not restarted when a new version is detected.  
| score_logging_steps | 0                  | The number of steps until scores are logged. If 0, no logging will be performed. |         
| score_logging_file  | "scores.csv"           | Scores will be logged to the specified file.     |                                                                             

## Optional: API
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

```curl
curl -X POST http://127.0.0.1:9999/translate \
     -H "auth: change-me" \
     -H "Content-Type: application/json" \
     -d '{"source_texts": ["hello world"], "source_lang": "auto", "target_lang": "es"}'
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