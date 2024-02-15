from bittranslate.content_filter import (
    contains_url,
    contains_author_list,
    contains_formula,
)


def test_contains_url_true():
    text = "Check out this website: https://example.com"
    assert contains_url(text) is True


def test_contains_url_false():
    text = "This text does not contain a URL."
    assert contains_url(text) is False


def test_likely_author_list_true():
    text = "Author(s) M. Maniwalla, K. K. Munger, M. Kothar, D. J. Gupta, and P. S. Chattopadhyay Abstract Background FAT is one of the most widely used methods to analyze"
    assert contains_author_list(text) is True


def test_likely_author_list_false():
    text = "This text does not contain an author list."
    assert contains_author_list(text) is False


def test_contains_formula_true():
    text = "A) X + 2NaNO3 B) X = 3NaNO5 C) X - 5NaNO2 D) X X D) 3Na + 2OH X -2 + NaOH X + 3 + NaO3 X + 4 - NaOH 6 X + 6HNO2 + H"
    assert contains_formula(text) is True


def test_contains_formula_false():
    text = "This text does not contain a formula."
    assert contains_formula(text) is False
