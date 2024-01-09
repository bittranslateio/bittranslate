from .validator import validator

chinese_text = """作者 孙玉华 ; 李建强 ; 杨志强 机构 南京大学 ; [南京]中国科学院信息工程研究所 ; [上海]中国电子科技"""


def test_is_gibberish_true():
    assert validator._is_gibberish(chinese_text, lang="en") is True


def test_is_gibberish_zh_false():
    assert validator._is_gibberish(chinese_text, lang="zh") is False


def test_is_gibberish_false():
    text = "In the present work we demonstrate that the proposed lossy encoding method achieves a better performance for low-energy devices."
    assert validator._is_gibberish(text, lang="en") is False
