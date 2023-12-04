from .validator import validator


def test_select_lang_pair():
    lang_pair = validator._select_lang_pair()
    assert lang_pair in validator._lang_pairs

    # 95% of pair should be part of the old group
    pairs = []
    for i in range(0, 10000):
        pairs.append(validator._select_lang_pair())

    old_pairs = []
    for pair in pairs:
        if pair in validator._prior_lang_pairs:
            old_pairs.append(pair)


    assert 9250 <= len(old_pairs) <= 9750



