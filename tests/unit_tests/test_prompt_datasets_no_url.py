import pytest
from bittranslate import Exams, XQuAD, PeerSum, GermanQuAD, MKqa, BitTranslateDataset
from langdetect import detect

def assert_no_urls(result: str):
    """
    Checks that the given string does not contain "http" or "https".

    Args:
        result: The string to check for URL presence.
    """

    assert not any(url in result for url in ("http", "https"))


def check_dataset_sample(dataset_class: object, valid_langs: list):
    """
    Tests sample generation and absence of URLs for the given dataset.

    Args:
        dataset_class: The dataset class to test.
        valid_langs: A list of valid languages supported by the dataset.
    """

    dataset_object = dataset_class()

    # Test sample generation and no URLs for valid languages
    for expect_lang in valid_langs:
        result = dataset_object.sample_case(expect_lang)
        assert type(result) == str  # Ensure result is a string

        assert_no_urls(result)  # Check for absence of URLs


@pytest.mark.parametrize(
    "dataset_class, valid_langs",
    [
        (PeerSum, ["en"]),  # Test PeerSum
        (GermanQuAD, ["de"]),  # Test GermanQuAD
        (Exams, ["bg", "hu", "it", "pl", "pt", "tr", "vi"]),  # Test Exams
        (XQuAD, ["ar", "de", "el", "en", "es", "hi", "ro", "ru", "th", "tr", "vi", "zh"]),  # Test XQuAD
        (MKqa, ["fr"]),  # Test MKqa
        (BitTranslateDataset, ["et", "fa", "fi", "fr", "ko", "sv", "uk"]),  # Test BitTranslateDataset
    ],
)
def test_dataset_samples(dataset_class, valid_langs):
    """
    Parametrized test for different datasets and languages.

    Args:
        dataset_class: The dataset class to test.
        valid_langs: A list of valid languages for the dataset.
    """

    check_dataset_sample(dataset_class, valid_langs)
