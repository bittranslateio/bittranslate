from bittranslate import RewardModel
from .test_score import run_test_score
from .validator import validator
from math import factorial


def test_valid_reward_models():
    assert all(isinstance(reward_model, RewardModel) for reward_model in validator._reward_models)

def test_reward_weights():
    assert sum(validator._reward_weights) == 1



def test_validator():
    # tests the single_score method
    run_test_score(validator, True)


def test_scores_en_pl():
    source_texts = ["This is example text.", "I am at my desk"]

    translated_texts = [["To jest przykładowy tekst",
                        "To jest przykładowa powieść.",
                        "To jest ołówek",
                        "This is the wrong language"],
                        [
                        "Jestem przy biurku",
                        "Stoję przy biurku",
                        "Nie ma mnie przy biurku",
                        "Wrong language"
                        ]
                        ]
    source_lang = "en"

    target_lang = "pl"

    scores, _, _ = validator.score(source_texts, translated_texts, source_lang, target_lang )
    assert type(scores) == list
    assert all(isinstance(score, float) for score in scores)
    # translated texts is in descending order by quality of the translations
    assert all(scores[i] > scores[i + 1] for i in range(len(scores) - 1))

    translated_texts_reversed = translated_texts.copy()
    for miner_results in translated_texts_reversed:
        miner_results.reverse()

    scores_reversed, _, _ = validator.score(source_texts, translated_texts_reversed, source_lang, target_lang)
    assert all(scores_reversed[i] < scores_reversed[i + 1] for i in range(len(scores_reversed) - 1))
    validator.save_tracked_results()



def test_scores_pl_en():
    source_texts = ["To jest przykładowy tekst", "Piszę oprogramowanie."]

    translated_texts = [["This is example text.",
                        "This is a sample novel.",
                        "This is pencil.",
                        "To jest niewłaściwy język."],

                        ["I am writing software.",
                        "I am coding right now.",
                        "I'm standing at the desk.",
                        "Zły język."]
                    ]
    source_lang = "pl"
    target_lang = "en"

    scores, top_translations, _ = validator.score(source_texts, translated_texts, source_lang, target_lang )
    assert top_translations[0] == "This is example text."
    assert top_translations[1] == "I am writing software."

    assert type(scores) == list
    assert all(isinstance(score, float) for score in scores)
    # translated texts is in descending order by quality of the translations
    assert all(scores[i] > scores[i + 1] for i in range(len(scores) - 1))

    translated_texts_reversed = translated_texts.copy()
    for miner_results in translated_texts_reversed:
        miner_results.reverse()

    scores_reversed, _, _ = validator.score(source_texts, translated_texts_reversed, source_lang, target_lang)
    print(scores_reversed)
    print(translated_texts_reversed)
    assert all(scores_reversed[i] < scores_reversed[i + 1] for i in range(len(scores_reversed) - 1))

def test_unique_langs():
    assert len(validator._langs) == len(set(validator._langs))


def test_lang_pairs():
    n  = len(validator._langs)
    expected_permutations = factorial(n) // factorial(n - 2)

    assert len(validator._lang_pairs) == expected_permutations
    seen = set()
    for sublist in validator._lang_pairs:
        # Length must be 2, with a source and a target lang.
        assert len(sublist) == 2
        # All unique
        tuple_lang_pair = tuple(sublist)
        assert tuple_lang_pair not in seen
        seen.add(tuple_lang_pair)

        # Source does not equal target
        assert sublist[0] != sublist[1]

        # Source is valid
        assert sublist[0] in validator._langs

        # Target is valid
        assert sublist[1] in validator._langs

