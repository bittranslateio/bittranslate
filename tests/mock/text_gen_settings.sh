#!/bin/bash
#Greedy Decoding: Greedy decoding (default)
echo "Greedy"
python run_miner.py

# Top-k Sampling  with high k
echo "Top-k (100) sampling"
python run_miner.py --do_sample --top_k 100

# Top-k Sampling  with low k
echo "Top-k (10) sampling"
python run_miner.py --do_sample --top_k 10

#Beam-Search
echo "Beam search"
python run_miner.py --num_beams 5

