from bittranslate import Tracker

def compare_list(l1, l2):
    assert [i for i, j in zip(l1, l2) if i == j]
    
def test_tracker():
    mock_lang_pairs = [["en", "pl"], ["pl", "en"]]
    tracker = Tracker(mock_lang_pairs, 2)

    en_top_min_source_1 = "min source 1"
    en_top_min_translation_1 = "min translation 1"
    en_top_min_score_1 = 0.1
    en_top_max_source_1= "max source 1"
    en_top_max_translation_1 = "max translation 1"
    en_top_max_score_1  = 0.7

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
    en_top_max_score_2  = 0.8

    tracker.track_texts("en", "pl", en_top_min_source_2, en_top_min_translation_2, en_top_min_score_2, en_top_max_source_2, en_top_max_translation_2, en_top_max_score_2)
    
    en_top_min_source_3 = "min source 3"
    en_top_min_translation_3 = "min translation 3"
    en_top_min_score_3 = 0.3
    en_top_max_source_3 = "max source 3"
    en_top_max_translation_3 = "max translation 3"
    en_top_max_score_3  = 0.9

    tracker.track_texts("en", "pl", en_top_min_source_3, en_top_min_translation_3, en_top_min_score_3, en_top_max_source_3, en_top_max_translation_3, en_top_max_score_3)
    
    
    pl_top_min_source_1 = "pl min source 1"
    pl_top_min_translation_1  = "pl min translation 1"
    pl_top_min_score_1  = 0.3
    pl_top_max_source_1  = "pl max source 1"
    pl_top_max_translation_1  = "pl max translation 1"
    pl_top_max_score_1   = 0.9
    tracker.track_texts("pl", "en", pl_top_min_source_1 ,
                        pl_top_min_translation_1 , 
                        pl_top_min_score_1 ,
                        pl_top_max_source_1 , 
                        pl_top_max_translation_1 , 
                        pl_top_max_score_1 )
    
    # en
    track_en_pl_min = tracker.text_tracking["en_pl"]["min"]
    track_en_pl_max = tracker.text_tracking["en_pl"]["max"]

    # en min
    expected = [en_top_min_source_2, en_top_min_source_3]
    compare_list(track_en_pl_min["sources"],  expected)
    
    expected = [en_top_min_translation_2, en_top_min_translation_3]
    compare_list(track_en_pl_min["translations"],  expected)
    
    expected = [en_top_min_score_2, en_top_min_score_3]
    compare_list(track_en_pl_min["scores"],  expected)


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

    tracker.texts_to_json()




