# Simulation Testing
You can use the "run_miner.py" script to gauge the performance of your miner. 
The script simulates the main network by running the code validators use to generate cases and score responses. 
It prints the average time it takes the miner to produce a response along with the average score according to the internal validator. 

The script uses the miner located at  ```from neurons.miners.m2m_miner import M2MMiner``` and so you can modify the same parameters this miner includes. 
For example, you can adjust the model by supplying a Hugging Face ID to the "model_name" parameter like "facebook/m2m100_418M". 
You can also go a step further by modifying the code for M2MMiner to attempt to find improvements. 

```bash
python3 simulate/run_miner --rounds 100
```

## Parameters 

### Script 

| Parameter  | Default | Description                                              |
|------------|---------|----------------------------------------------------------|
| rounds     | 100     | The number of cases that will be produced evaluated      |
| val_device | "cuda"  | What device to use for the the validator's Reward Models | 
| save_data  | None    | A path to a JSON file to save generated  data            | 
| load_data  | None    | A path to a JSON file to load  data                      | 


### M2MMiner
The script inherits the parameters from M2MMiner. Below are parameters that are relevant to the script. 

| Parameter                                 | Default                | Description                                                                                   |
|-------------------------------------------|------------------------|-----------------------------------------------------------------------------------------------|
| device                                    | "cuda"                 | What device to use for the miner's model.                                                     | 
| model_name                                | "facebook/m2m100_1.2B" | Either a Hugging Face ID or a path to a local path that contains both the model and tokenizer |

## Saving and loading data 
To improve the consistency of your runs you can save the data generated from your first run and re-use it for subsequent runs.  

### First run: 
```bash
python3 simulate/run_miner --rounds 100 --save_data "saved_data.json"
```

### Subsequent runs:
```bash
python3 simulate/run_miner --load_data "saved_data.json"
```


