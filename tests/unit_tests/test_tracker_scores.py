from bittranslate import Tracker

def compare_list(l1, l2):
    assert [i for i, j in zip(l1, l2) if i == j]

def test_create_lang_pair_key():
    assert Tracker._create_lang_pair_key("en", "pl") == "en_pl"

def test_tracker():
    mock_lang_pairs = [["en", "pl"], ["pl", "en"]]
    tracker = Tracker(mock_lang_pairs, 2)
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





