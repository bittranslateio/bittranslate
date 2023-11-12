from datasets import load_dataset
from .prompt_dataset import PromptDataset
import random


class XQuAD(PromptDataset):
    def __init__(self):
        super().__init__()
        self._dataset_de = load_dataset("xquad", "xquad.de", split="validation")
        self._dataset_en = load_dataset("xquad", "xquad.en", split="validation")
        self._dataset_es = load_dataset("xquad", "xquad.es", split="validation")

        self._dataset_len_de = len(self._dataset_de)
        self._dataset_len_en = len(self._dataset_en)
        self._dataset_len_es = len(self._dataset_es)

        self._valid_ln = ["de", "en", "es"]

    def sample_case(self, language="en") -> str:
        if language not in self._valid_ln:
            raise ValueError(
                f"{language} is an invalid language. Valid languages include {self._valid_ln}"
            )

        if language == "de":
            random_index = random.randint(0, self._dataset_len_de - 1)
            return self._dataset_de[random_index]["question"]
        elif language == "en":
            random_index = random.randint(0, self._dataset_len_en - 1)
            return self._dataset_en[random_index]["question"]
        else:
            # implied "es"
            random_index = random.randint(0, self._dataset_len_es - 1)
            return self._dataset_es[random_index]["question"]