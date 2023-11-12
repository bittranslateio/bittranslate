from .validator import validator


def test_generate_cases():
    source_lang, target_lang, sources = validator.generate_cases(count=2)
    assert type(sources) == list
    assert len(sources) == 2

    assert type(sources[0]) == str
    assert type(source_lang) == str
    assert type(target_lang) == str

    for source in sources:
        tokens = validator._mgpt_pipeline.tokenizer.encode(source)
        token_len = len(tokens)
        assert 50 <= token_len <= 100


