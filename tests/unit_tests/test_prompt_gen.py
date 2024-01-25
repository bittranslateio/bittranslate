from .validator import validator
from bittranslate.util import trim_prompt
#this is based on self.lang in validator
#langs_to_test = ["ar", "bg", "de", "el", "en", "es", "hi", "hu", "it", "pl", "pt","ro", "ru", "th",  "tr", "vi", "fr","zh"]
langs_to_test = ['en','zh']

def test_prompt_gen():
    for l in langs_to_test:
        if(l=='zh'):
            result = validator._generate_prompt("你好世界", lang=l)
            assert type(result) == str
            token_output = validator._wenzhong_gpt2_pipeline.tokenizer.encode(result)
        elif(l=='en'):
            result = validator._generate_prompt("hello world", lang = l)
            assert type(result) == str
            token_output = validator._mgpt_pipeline.tokenizer.encode(result)
        token_len = len(token_output)
        assert 50 <= token_len <= 100

def test_generate_prompts():
    for l in langs_to_test:
        if(l=='zh'):
            texts = ["写一个故事：", "写一首歌："]
            tokenizer = validator._wenzhong_gpt2_pipeline.tokenizer
        elif(l=='en'):
            texts = ["Write a story:", "Write a song:"]
            tokenizer = validator._mgpt_pipeline.tokenizer
        else:
            print('lang not set with default texts')
        prompts = []
        for text in texts:
            prompts.append(validator._generate_prompt(text, lang = l))
        assert texts[0] not in prompts[0]
        assert texts[1] not in prompts[1]
        assert type(prompts) == list
        assert len(prompts) == 2
        assert type(prompts[0]) == str
        for prompt in prompts:
            token_output = tokenizer.encode(prompt)
            token_len = len(token_output)
            assert 50 <= token_len <= 100

def test_trim_prompt():
    toks = ["t1", "t2", "t3"]
    result =  trim_prompt(toks,2)
    assert result == ["t2", "t3"]

    result =  trim_prompt(toks,4)
    assert result == ["t1", "t2", "t3"]
