from .validator import validator

def test_prompt_gen():
    result = validator._generate_prompt("hello world")
    assert type(result) == str
    token_output = validator._mgpt_pipeline.tokenizer.encode(result)
    token_len = len(token_output)
    assert 50 <= token_len <= 100

def test_generate_prompts():


    texts = ["Write a story:", "Write a song:"]
    prompts = []
    for text in texts:
        prompts.append(validator._generate_prompt(text))
    assert texts[0] not in prompts[0]
    assert texts[1] not in prompts[1]
    assert type(prompts) == list
    assert len(prompts) == 2
    assert type(prompts[0]) == str
    for prompt in prompts:
        token_output = validator._mgpt_pipeline.tokenizer.encode(prompt)
        token_len = len(token_output)
        assert 50 <= token_len <= 100
