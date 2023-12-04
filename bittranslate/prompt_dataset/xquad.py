from typing import Dict

from datasets import Dataset, load_dataset
from .prompt_dataset import PromptDataset
import random

LANGUAGES = [ 
    'ar', 'de', 'el', 'en', 'es', 'hi', 'ro', 'ru', 'th', 'tr', 'vi' 
]

class XQuAD(PromptDataset):

    _datasets: Dict[str, Dataset]
    """ Map of datasets by language. """

    def __init__(self):
        super().__init__()

        self._datasets = {
            language : load_dataset("xquad", f"xquad.{language}", split="validation")
            for language in LANGUAGES
        }

    def sample_case(self, language="en") -> str:
        if language not in self._datasets:
            raise ValueError(
                f"{language} is an invalid language. "
                f"Valid languages include {list(self._datasets.keys())}"
            )
        
        row = random.choice(self._datasets[language])
        return row["question"]