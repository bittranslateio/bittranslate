from .validator import validator

def test_filter_lang():
    translated_text = ["Let's write some code today.", "Napiszmy dzisiaj trochę kodu.", "I am looking forward to coding.", "Nie mogę się doczekać kodowania."]
    result_en = validator._filter_lang(translated_text, "en")
    expected_result_en = [1, 0, 1, 0]
    assert result_en == expected_result_en

    result_pl = validator._filter_lang(translated_text, "pl")
    expected_result_pl = [0, 1, 0, 1]
    assert result_pl == expected_result_pl

    pl_source_text = ["Napiszmy dzisiaj trochę kodu."]*4
    scores_pl_en, _, _ = validator.score(pl_source_text, [translated_text], "en")
    assert scores_pl_en[0] > 0
    assert scores_pl_en[1] == 0
    assert scores_pl_en[2] > 0
    assert scores_pl_en[3] == 0

    en_source_text = ["Let's write some code today."]*4
    scores_pl_en, _, _ = validator.score(en_source_text, [translated_text], "pl")
    assert scores_pl_en[0] == 0
    assert scores_pl_en[1] > 0
    assert scores_pl_en[2] == 0
    assert scores_pl_en[3] > 0