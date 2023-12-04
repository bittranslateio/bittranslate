from bittranslate import MiningTracker

def compare_list(l1, l2):
    assert [i for i, j in zip(l1, l2) if i == j]

def test_mining_tracker():
    mock_lang_pairs = [["en", "pl"], ["pl", "en"]]

    mining_tracker = MiningTracker(lang_pairs=mock_lang_pairs, n=2)

    source_0 = ["source 0: 0", "source 0: 1"]
    translated_0 = ["translated 0: 0", "translated 0: 1"]
    mining_tracker.track_texts("en", "pl", source_0, translated_0)
    compare_list(mining_tracker.text_tracking["en_pl"][0]["source_texts"], source_0)
    compare_list(mining_tracker.text_tracking["en_pl"][0]["translated_texts"], translated_0)
    assert len(mining_tracker.text_tracking["en_pl"]) == 1

    source_1 = ["source 1: 0", "source 1: 1"]
    translated_1 = ["translated 1: 0", "translated 1: 1"]
    mining_tracker.track_texts("en", "pl", source_1, translated_1)
    compare_list(mining_tracker.text_tracking["en_pl"][1]["source_texts"], source_1)
    compare_list(mining_tracker.text_tracking["en_pl"][1]["translated_texts"], translated_1)

    source_2 = ["source 2: 0", "source 2: 1"]
    translated_2 = ["translated 2: 0", "translated 2: 1"]
    mining_tracker.track_texts("en", "pl", source_2, translated_2)
    compare_list(mining_tracker.text_tracking["en_pl"][0]["source_texts"], source_1)
    compare_list(mining_tracker.text_tracking["en_pl"][0]["translated_texts"], translated_1)

    assert len(mining_tracker.text_tracking["en_pl"]) == 2
    compare_list(mining_tracker.text_tracking["en_pl"][1]["source_texts"], source_2)
    compare_list(mining_tracker.text_tracking["en_pl"][1]["translated_texts"], translated_2)

    source_3 = ["source 3: 0", "source 3: 1"]
    translated_3 = ["translated 3: 0", "translated 3: 1"]
    mining_tracker.track_texts("pl", "en", source_3, translated_3)
    assert len(mining_tracker.text_tracking["pl_en"]) == 1
    compare_list(mining_tracker.text_tracking["pl_en"][0]["source_texts"], source_3)
    compare_list(mining_tracker.text_tracking["pl_en"][0]["translated_texts"], translated_3)

    mining_tracker.texts_to_json("outputs/texts_miner.json")