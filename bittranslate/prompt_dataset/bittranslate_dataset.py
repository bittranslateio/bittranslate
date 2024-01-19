from typing import Dict

from datasets import Dataset, load_dataset
from .prompt_dataset import PromptDataset
import random


language_details_by_code = {
    'et': {'language': 'Estonian', 'dataset_name': 'BitTranslate/chatgpt-prompts-Estonian',
           'features': ['act', 'prompt']},
    'fa': {'language': 'Persian', 'dataset_name': 'BitTranslate/chatgpt-prompts-Persian',
           'features': ['act', 'prompt']},
    'fi': {'language': 'Finnish', 'dataset_name': 'BitTranslate/chatgpt-prompts-Finnish', 'features': ['act', 'prompt']},
    'fr': {'language': 'French', 'dataset_name': 'BitTranslate/chatgpt-prompts-French', 'features': ['act', 'prompt']},
    'ko': {'language': 'Korean', 'dataset_name': 'BitTranslate/chatgpt-prompts-Korean', 'features': ['역할', '프롬프트']},
    'sv': {'language': 'Swedish', 'dataset_name': 'BitTranslate/chatgpt-prompts-Swedish', 'features': ['act', 'prompt']},
    'uk': {'language': 'Ukrainian', 'dataset_name': 'BitTranslate/chatgpt-prompts-Ukrainian', 'features': ['дія', 'запит']},
}


class BitTranslateDataset(PromptDataset):
    _datasets: Dict[str, Dataset]

    def __init__(self):
        super().__init__()

        self._datasets = {
            language: load_dataset(lang_details['dataset_name'], split='train')
            for language, lang_details in language_details_by_code.items()
        }

    def sample_case(self, language="fi") -> str:
        if language not in self._datasets:
            raise ValueError(
                f"{language} is an invalid language. "
                f"Valid languages include {list(self._datasets.keys())}"
            )

        row = random.choice(self._datasets[language])
        # The prompt category is always second index of the list under the the features key.
        return row[language_details_by_code[language]['features'][1]]