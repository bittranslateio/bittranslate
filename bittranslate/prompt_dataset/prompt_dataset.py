from abc import abstractmethod


class PromptDataset:
    def __init__(self):
        pass

    @abstractmethod
    def sample_case(self) -> str:
        pass
