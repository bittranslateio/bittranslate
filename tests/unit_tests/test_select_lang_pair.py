from collections import defaultdict

from .validator import validator


def test_select_lang_pair():
    lang_probs = validator._lang_probs
    lang_pair = validator._select_lang_pair()
    assert lang_pair in validator._lang_pairs, f"{lang_pair} is not in lang pairs"
    assert (
        lang_pair[0] != lang_pair[1]
    ), "The two languages in the pair should be different"

    trial = defaultdict(lambda: 0)
    n = 10000
    for _ in range(n):
        source_lang, target_lang = validator._select_lang_pair()
        assert (source_lang, target_lang) in validator._lang_pairs
        trial[source_lang] += 1

    eps = 0.05
    for lang, prob in lang_probs.items():
        real_dist = trial[lang] / n
        assert (
            abs(real_dist - prob) < eps
        ), f"Probability of '{lang}'({real_dist}) does not match expected distribution of {prob}"

    remaining_prob = 1 - sum(lang_probs.get(lang, 0) for lang in validator._langs)
    others_prob = sum([v for k, v in trial.items() if k not in lang_probs.keys()]) / n
    assert (
        abs(others_prob - remaining_prob) < eps
    ), f"Probability of 'other'({others_prob}) does not match expected distribution of {remaining_prob}"
