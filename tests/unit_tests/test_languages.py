from .validator import validator


def test_langs():
    langs = validator._langs

    datasets = validator._datasets
    datasets_keys = list(datasets.keys())
    langs.sort()
    datasets_keys.sort()

    assert langs == datasets_keys

    for lang_code, datasets in datasets.items():
        for dataset in datasets:
            assert type(dataset.sample_case(lang_code)) == str





