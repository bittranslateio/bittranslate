import json
from .validator import validator
from bittranslate.detect_lang import DetectLang

def test_filter_lang():
    translated_text = ["Let's write some code today.", "Napiszmy dzisiaj trochę kodu.", "I am looking forward to coding.", "Nie mogę się doczekać kodowania."]
    result_en = validator._filter_lang(translated_text, "pl", "en")
    expected_result_en = [1, 0, 1, 0]
    assert result_en == expected_result_en

    result_pl = validator._filter_lang(translated_text, "en", "pl")
    expected_result_pl = [0, 1, 0, 1]
    assert result_pl == expected_result_pl

    pl_source_text = "Napiszmy dzisiaj trochę kodu."
    scores_pl_en  = validator.single_score(pl_source_text, translated_text, "pl", "en")
    assert scores_pl_en[0] > 0
    assert scores_pl_en[1] == 0.0
    assert scores_pl_en[2] > 0
    assert scores_pl_en[3] == 0.0

    en_source_text = "Let's write some code today."
    scores_en_pl = validator.single_score(en_source_text, translated_text, "en", "pl")
    assert scores_en_pl[0] == 0.0
    assert scores_en_pl[1] > 0
    assert scores_en_pl[2] == 0.0
    assert scores_en_pl[3] > 0

def test_detect_lang():
    save_path = 'outputs/detect_lang.json'
    detect_lang = DetectLang('outputs/detect_lang.json')
    text = "Hello world. Let's write some code"
    detect_lang.detect(text, "pl", "en")
    detect_lang.detect(text, "pl", "en")
    detect_lang.detect(text, "en", "pl")
    detect_lang.detect(text, "en", "pl")

    with open(save_path, 'r') as file:
        data = json.load(file)

    assert data["pass"]['source']['pl'] == 2
    assert data["pass"]['target']['en'] == 2

    assert data["fail"]['source']['en'] == 2
    assert data["fail"]['target']['pl'] == 2

    assert data["pass"]['source-target']['pl-en'] == 2
    assert data["fail"]['source-target']['en-pl'] == 2

    assert data["count"] == 4

    assert data["pass"]['count'] == 2
    assert data["fail"]['count'] == 2

