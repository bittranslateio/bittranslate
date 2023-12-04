from bittranslate import ValidatorTracker

def compare_list(l1, l2):
    assert [i for i, j in zip(l1, l2) if i == j]

def test_validator_create_lang_pair_key():
    assert ValidatorTracker._create_lang_pair_key("en", "pl") == "en_pl"

def test_validator_scores_tracker():
    mock_lang_pairs = [["en", "pl"], ["pl", "en"]]
    tracker = ValidatorTracker(mock_lang_pairs, 2)
    expected_lang_pairs = ["en_pl", "pl_en"]
    compare_list(tracker.score_tracking.keys(), expected_lang_pairs)

    first_scores = [0, 0.5]
    tracker.track_scores("en", "pl", first_scores)
    r = tracker.score_tracking["en_pl"]
    assert r['mean'] == sum(first_scores)/ len(first_scores)
    assert r['average_max_score'] == max(first_scores)
    assert r['average_min_score'] == min(first_scores)

    second_scores = [0.5, 1.0]
    tracker.track_scores("en", "pl", second_scores)
    r = tracker.score_tracking["en_pl"]
    included_scores = first_scores + second_scores

    assert r['mean'] == sum(included_scores)/ len(included_scores)
    assert r['average_max_score'] ==  (0.5 + 1)/2
    assert r['average_min_score'] ==  (0 + 0.5)/2

    third_scores = [0.2, 0.1]
    tracker.track_scores("en", "pl", third_scores)
    r = tracker.score_tracking["en_pl"]
    included_scores = second_scores + third_scores
    assert r['mean'] == sum(included_scores) / len(included_scores)
    assert r['average_max_score'] == (1+0.2)/2
    assert r['average_min_score'] == (0.5+0.1)/2

    fourth_scores = [0.3, 0.5]
    tracker.track_scores("pl", "en", fourth_scores)
    r = tracker.score_tracking["pl_en"]
    assert r['mean'] == sum(fourth_scores) / len(fourth_scores)
    assert r['average_max_score'] == 0.5
    assert r['average_min_score'] == 0.3
    tracker.scores_to_json("outputs/scores_validator.json")

def test_validator_texts_tracker():
    mock_lang_pairs = [["en", "pl"], ["pl", "en"]]
    tracker = ValidatorTracker(mock_lang_pairs, 2)

    en_top_min_source_1 = "min source 1"
    en_top_min_translation_1 = "min translation 1"
    en_top_min_score_1 = 0.1
    en_top_max_source_1 = "max source 1"
    en_top_max_translation_1 = "max translation 1"
    en_top_max_score_1 = 0.7

    tracker.track_texts("en", "pl", en_top_min_source_1,
                        en_top_min_translation_1,
                        en_top_min_score_1,
                        en_top_max_source_1,
                        en_top_max_translation_1,
                        en_top_max_score_1)

    en_top_min_source_2 = "min source 2"
    en_top_min_translation_2 = "min translation 2"
    en_top_min_score_2 = 0.2
    en_top_max_source_2 = "max source 2"
    en_top_max_translation_2 = "max translation 2"
    en_top_max_score_2 = 0.8

    tracker.track_texts("en", "pl", en_top_min_source_2, en_top_min_translation_2, en_top_min_score_2,
                        en_top_max_source_2, en_top_max_translation_2, en_top_max_score_2)

    en_top_min_source_3 = "min source 3"
    en_top_min_translation_3 = "min translation 3"
    en_top_min_score_3 = 0.3
    en_top_max_source_3 = "max source 3"
    en_top_max_translation_3 = "max translation 3"
    en_top_max_score_3 = 0.9

    tracker.track_texts("en", "pl", en_top_min_source_3, en_top_min_translation_3, en_top_min_score_3,
                        en_top_max_source_3, en_top_max_translation_3, en_top_max_score_3)

    pl_top_min_source_1 = "pl min source 1"
    pl_top_min_translation_1 = "pl min translation 1"
    pl_top_min_score_1 = 0.3
    pl_top_max_source_1 = "pl max source 1"
    pl_top_max_translation_1 = "pl max translation 1"
    pl_top_max_score_1 = 0.9
    tracker.track_texts("pl", "en", pl_top_min_source_1,
                        pl_top_min_translation_1,
                        pl_top_min_score_1,
                        pl_top_max_source_1,
                        pl_top_max_translation_1,
                        pl_top_max_score_1)

    # en
    track_en_pl_min = tracker.text_tracking["en_pl"]["min"]
    track_en_pl_max = tracker.text_tracking["en_pl"]["max"]

    # en min
    expected = [en_top_min_source_2, en_top_min_source_3]
    compare_list(track_en_pl_min["sources"], expected)

    expected = [en_top_min_translation_2, en_top_min_translation_3]
    compare_list(track_en_pl_min["translations"], expected)

    expected = [en_top_min_score_2, en_top_min_score_3]
    compare_list(track_en_pl_min["scores"], expected)

    # en max
    expected = [en_top_max_source_2, en_top_max_source_3]
    compare_list(track_en_pl_max["sources"], expected)

    expected = [en_top_max_translation_2, en_top_max_translation_3]
    compare_list(track_en_pl_max["translations"], expected)

    expected = [en_top_max_score_2, en_top_max_score_3]
    compare_list(track_en_pl_max["scores"], expected)

    # pl
    track_pl_en_min = tracker.text_tracking["pl_en"]["min"]
    track_pl_en_max = tracker.text_tracking["pl_en"]["max"]

    # en min
    expected = [pl_top_min_source_1]
    compare_list(track_pl_en_min["sources"], expected)

    expected = [pl_top_min_translation_1]
    compare_list(track_pl_en_min["translations"], expected)

    expected = [pl_top_min_score_1]
    compare_list(track_pl_en_min["scores"], expected)

    # en max
    expected = [pl_top_max_source_1]
    compare_list(track_pl_en_max["sources"], expected)

    expected = [pl_top_max_translation_1]
    compare_list(track_pl_en_max["translations"], expected)

    expected = [pl_top_max_score_1]
    compare_list(track_pl_en_max["scores"], expected)

    tracker.texts_to_json("outputs/texts_validator.json")