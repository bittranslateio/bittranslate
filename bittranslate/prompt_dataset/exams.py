from datasets import load_dataset
from .prompt_dataset import PromptDataset
import random


class Exams(PromptDataset):
    def __init__(self):
        super().__init__()
        self._dataset = load_dataset("exams", "multilingual", split="train")
        target_langs = ["Italian", "Polish"]
        # remove any potential None None values
        self._dataset = self._dataset.filter(
            lambda record: record["question"]["stem"] is not None and record["info"]["language"] is not None)

        self._dataset_it = self._dataset .filter(
            lambda record: record["info"]["language"] =="Italian"
        )

        self._dataset_pl = self._dataset.filter(
            lambda record: record["info"]["language"] == "Polish"
        )

        self._dataset_len_it = len(self._dataset_it)
        self._dataset_len_pl = len(self._dataset_pl)
        self._valid_ln = ["it", "pl"]

    def sample_case(self, language="en") -> str:
        if language not in self._valid_ln:
            raise ValueError(
                f"{language} is an invalid language. Valid languages include {self._valid_ln}"
            )
        if language=="it":
            random_index = random.randint(0, self._dataset_len_it - 1)
            return self._dataset_it[random_index]["question"]["stem"]
        else:
            # implied "pl"
            random_index = random.randint(0, self._dataset_len_pl - 1)
            return self._dataset_pl[random_index]["question"]["stem"]