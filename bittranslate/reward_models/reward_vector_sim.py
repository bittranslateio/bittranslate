from sentence_transformers import SentenceTransformer, util
from .reward_model import RewardModel
from typing import List


class VectorSim(RewardModel):
    def __init__(self, device: str="cpu"):
        super().__init__()
        self._sent_trans_model = SentenceTransformer("sentence-transformers/LaBSE", device=device)

    def score(self, source_text: str, translated_text: List[str]) -> List[float]:
        en_source = self._sent_trans_model.encode(source_text)
        en_translated = self._sent_trans_model.encode(translated_text)
        scores = util.cos_sim(en_source, en_translated)
        # there's only once source text, and so we return the first element of scores.
        return scores[0].tolist()
