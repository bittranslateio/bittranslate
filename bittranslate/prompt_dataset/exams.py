import random
from typing import Dict

from datasets import Dataset, load_dataset
from .prompt_dataset import PromptDataset

LANGUAGE_SHORTHANDS = {
    "bg": "Bulgarian",
    "hu": "Hungarian",
    "it": "Italian",
    "pl": "Polish",
    "pt": "Portuguese",
    "tr": "Turkish",
    "vi": "Vietnamese"
}

class Exams(PromptDataset):

    lang_datasets: Dict[str, Dataset]
    """ Map of language shorthand to dataset filtered for said language. """

    def __init__(self):
        super().__init__()
        self._dataset = load_dataset("exams", "multilingual", split="train")
        # remove any potential None None values
        self._dataset = self._dataset.filter(
            lambda record: record["question"]["stem"] is not None and record["info"]["language"] is not None)

        self._lang_datasets = {
            shorthand : self._dataset.filter(
                lambda record: record["info"]["language"] == language
            )
            for shorthand, language in LANGUAGE_SHORTHANDS.items()
        }

    def sample_case(self, language="vi") -> str:
        if language not in self._lang_datasets:
            raise ValueError(
                f"{language} is an invalid language. "
                f"Valid languages include {list(self._lang_datasets.keys())}"
            )

        row = random.choice(self._lang_datasets[language])
        return row["question"]["stem"]