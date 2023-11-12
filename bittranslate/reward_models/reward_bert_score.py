from typing import List
from .reward_model import RewardModel
from bert_score import BERTScorer


class BertScore(RewardModel):
    def __init__(self, model_type: str="bert-base-multilingual-cased", device: str = "cpu"):
        super().__init__()
        self._device = device

        self._bert_score = BERTScorer(model_type=model_type, device=self._device)

    def score(self, source_text: str, translated_text: List[str]) -> List[float]:
        source_texts = [source_text] * len(translated_text)

        _, _, f1 = self._bert_score.score(source_texts, translated_text)

        return f1.tolist()
