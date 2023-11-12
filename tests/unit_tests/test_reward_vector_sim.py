from bittranslate import VectorSim
from .test_score import run_test_score

def test_reward_bert_score():
    vector_sim = VectorSim()
    run_test_score(vector_sim, False)






