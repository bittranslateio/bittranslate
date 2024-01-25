from typing import Union
from bittranslate import RewardModel
from .shared_data import SOURCE_TEXT, TRANSLATED_TEXTS
from bittranslate import Validator

def run_test_score(reward_model: Union[RewardModel, Validator], is_validator: bool = False):
    if is_validator:
        result = reward_model.single_score(SOURCE_TEXT, TRANSLATED_TEXTS, "en","pl")
    else:
        result = reward_model.score(SOURCE_TEXT, TRANSLATED_TEXTS)

    assert type(result) == list
    assert all(isinstance(score, float) for score in result)
    # TRANSLATED_TEXTS is in descending order by quality of the translation
    assert all(result[i] > result[i + 1] for i in range(len(result) - 1))

    translated_text_reverse = TRANSLATED_TEXTS.copy()
    translated_text_reverse.reverse()
    if is_validator:
        result_reversed = reward_model.single_score(SOURCE_TEXT, translated_text_reverse,"en", "pl")
    else:
        result_reversed = reward_model.score(SOURCE_TEXT, translated_text_reverse)

    assert all(result_reversed[i] < result_reversed[i + 1] for i in range(len(result_reversed) - 1))




