from typing import List
import bittensor as bt

def log_snippet_of_texts(texts: List[str], prefix) -> None:
    bt.logging.debug(f"len({prefix}) {len(texts)}")
    try:
        bt.logging.debug(f"{prefix}[0][:50]: {texts[0][:50]}")
    except Exception as e:
        bt.logging.debug("{prefix}}[0][:50]: INVALID")
    # Log the full source texts, but only at the TRACE logging level.
    bt.logging.trace(f"{prefix}: {texts}")