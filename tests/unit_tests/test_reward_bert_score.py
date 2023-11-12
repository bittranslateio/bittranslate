from bittranslate import BertScore
from .test_score import run_test_score

def test_reward_bert_score():
    bert_score = BertScore()
    run_test_score(bert_score, False)

