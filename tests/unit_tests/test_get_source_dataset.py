from bittranslate import Validator
from bittranslate import PromptDataset
from .validator import validator

def test_get_source_dataset():
    dataset, source, target = validator._get_source_dataset()
    assert issubclass(type(dataset), PromptDataset)
    assert type(source) == str
    assert type(target) == str
    source_target_pair = [source, target]
    assert source_target_pair in validator._lang_pairs




