import re


def contains_url(text: str):
    """Basic check for URLs"""
    return bool(re.search(r"https?://\S+|www\.\S+", text))


def contains_author_list(text: str):
    """Basic check for patterns resembling author lists"""
    author_names = re.findall(r"\b[A-Z]\. [A-Z][a-z]+", text)
    if len(author_names) > 1:
        return True
    return False


def contains_formula(text: str, threshold=0.1):
    """
    Check if the text contains chem formula patterns.
    """
    formula_patterns = [
        r"\b[A-Za-z0-9]+\([A-Za-z0-9]+\)",  # Matches expressions like function calls like H2O(l)
        r"\b[A-Za-z]+\d+",  # Matches chemical elements followed by numbers like H2
        r"\d+[A-Za-z]+",  # Matches numbers followed by letters, common in formulas like 2H
        r"\b\d{1,2}[A-Z]{1,2}\d?\b",  # Matches simple chemical formulas like H2O
        r"[\+\-\*/=^]",  # Matches mathematical operators like +, -, *, /, =, ^
    ]

    combined_pattern = "|".join(formula_patterns)
    matches = re.findall(combined_pattern, text)
    matched_length = sum(len(match) for match in matches)
    ratio = matched_length / len(text) if text else 0
    return ratio > threshold
