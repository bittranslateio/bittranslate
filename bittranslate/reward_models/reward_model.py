from abc import abstractmethod
from typing import List


class RewardModel:
    def __init__(self):
        pass

    @abstractmethod
    def score(self, source_text: str, translated_texts: List[str]) -> List[float]:
        pass
