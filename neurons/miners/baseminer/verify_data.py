from typing import TYPE_CHECKING, List, Tuple

from neurons.protocol import Translate

if TYPE_CHECKING:
    from .baseminer import BaseMiner


def verify_lang_pair(self: "BaseMiner", source_lang: str, target_lang: str) -> bool:
    for pair in self._lang_pairs:
        if source_lang == pair[0] and target_lang == pair[1]:
            return True
    else:
        return False


def verify_char_len(self: "BaseMiner", source_texts: List[str]) -> Tuple[bool, str]:
    for text in source_texts:
        char_count = len(text)
        if char_count >= self.config.max_char:
            return (
                False,
                f"Over character limit of {self.config.max_char} with {char_count} characters",
            )
        elif char_count == 0:
            return False, "Empty source text"

    return True, "verified!"


def verify_synapse_data(self, synapse: Translate) -> None:
    """Verify that the content of an incoming synapse
    is within the miner's configured limits.

    Raises `ValueError` if the synapse should not be serviced.

    This method is not to be confused with the axon's verify function,
    as this method requires knowledge of the synapse's data
    (from JSON payload rather than HTTP headers),
    which is only deserialized within the axon's forward function.
    """
    # confirm  language pair
    if not verify_lang_pair(self, synapse.source_lang, synapse.target_lang):
        raise ValueError(
            f"Request failed verification: Invalid language pair: {synapse.source_lang} -> {synapse.target_lang}"
        )
    # Confirm under char max and has at least 1 char.
    char_pass, reason = verify_char_len(self, synapse.source_texts)
    if not char_pass:
        raise ValueError(reason)

    if len(synapse.source_texts) > self.config.max_batch_size:
        raise ValueError(
            "Request failed verification: "
            f"{len(synapse.source_texts)=} "
            f"> {self.config.max_batch_size=}"
        )

    if not len(synapse.source_texts):
        raise ValueError("Source texts is of length 0")
