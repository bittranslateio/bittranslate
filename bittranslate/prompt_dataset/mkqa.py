from typing import Dict

from datasets import Dataset, load_dataset
from .prompt_dataset import PromptDataset
import random

language_codes_dict = {
    'French': 'fr'
}

LANGUAGES = list(language_codes_dict.values())


class MKqa(PromptDataset):

    _datasets: Dict[str, Dataset]
    """ Map of datasets by language. """

    def __init__(self):
        super().__init__()

        # Load and process the dataset for each language
        self._datasets = {
            language: self.process_dataset(language)
            for language in LANGUAGES
        }

    def process_dataset(self, language):
        dataset = load_dataset("mkqa", split="train")
        return [q[language] for q in dataset['queries'] if language in q]

    def sample_case(self, language="en") -> str:
        if language not in self._datasets:
            raise ValueError(
                f"{language} is an invalid language. "
                f"Valid languages include {list(self._datasets.keys())}"
            )
        
        row = random.choice(self._datasets[language])
        return row