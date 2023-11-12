from itertools import permutations
from neurons.miners.baseminer.baseminer import BaseMiner
from neurons.miners.baseminer.log_snippet import log_snippet_of_texts
from neurons.protocol import Translate
from transformers import (
    M2M100ForConditionalGeneration,
    M2M100Tokenizer
)
import argparse
import bittensor as bt
from bittranslate.logging import log_elapsed_time


class M2MMiner(BaseMiner):
    @classmethod
    def add_args(cls, parser: argparse.ArgumentParser) -> None:

        parser.add_argument(
            "--model_name",
            type=str,
            default="facebook/m2m100_1.2B",
            help="The Hugging Face ID or path to a model and tokenizer.",
        )

        parser.add_argument(
            "--device",
            type=str,
            default="cuda",
            help="What device to use, such as 'cpu' or 'cuda:0' ",
        )

        parser.add_argument(
            "--max_char",
            type=int,
            default=512,
            help="The maximum allowed characters for an incoming request.",
        )

        parser.add_argument(
            "--max_length",
            type=int,
            default=512,
            help="Maximum number of source tokens used for inference. Additional tokens will be truncated to this amount.",
        )

        parser.add_argument(
            "--max_batch_size",
            type=int,
            default=2,
            help=(
                "The maximum allowed batch size for an incoming request. "
                "Counted as number of source texts."
            ),
        )

    def __init__(self):
        super().__init__()
        bt.logging.info(f"Loading model {repr(self.config.model_name)}")
        self.model = M2M100ForConditionalGeneration.from_pretrained(
            self.config.model_name
        )

        if self.config.device != "cpu":
            self.model.to(self.config.device)

        self.tokenizer = M2M100Tokenizer.from_pretrained(self.config.model_name)

        self._langs = ["de", "en", "es", "it", "pl"]
        self._lang_pairs = list(permutations(self._langs, 2))

    def forward(self, synapse: Translate) -> Translate:
        # Verify the synapse has under max_batch_size source texts
        # that are all under max_char length.
        self.verify_synapse_data(synapse)

        source_lang = synapse.source_lang
        target_lang = synapse.target_lang
        bt.logging.debug(f"source_lang: {source_lang}")
        bt.logging.debug(f"target_lang: {target_lang}")

        # We have to set the language for the tokenizer to the source langauge.
        self.tokenizer.src_lang = source_lang

        log_snippet_of_texts(synapse.source_texts, "synapse.source_texts")

        # Tokenize the source texts,
        # as preparation for the text-to-text model.
        with log_elapsed_time("tokenize"):
            source_tok = self.tokenizer(
                synapse.source_texts,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=self.config.max_length,
            ).to(self.model.device)

        with log_elapsed_time("model_generate"):
            generated_tokens = self.model.generate(
                **source_tok,
                # To indicate to the language model
                # that we want to translate to a particular language,
                # we set the Beginning-Of-Stream (BOS) token.
                forced_bos_token_id=self.tokenizer.get_lang_id(target_lang),
            )

        with log_elapsed_time("detokenize"):
            decoded_texts = self.tokenizer.batch_decode(
                generated_tokens, skip_special_tokens=True
            )

        log_snippet_of_texts(decoded_texts, "decoded_texts")

        output_synapse = Translate(
            source_texts=synapse.source_texts,
            translated_texts=decoded_texts,
            source_lang=source_lang,
            target_lang=target_lang,
        )

        bt.logging.trace(f"output_synapse: {output_synapse}")

        return output_synapse

if __name__ == "__main__":
    M2MMiner().run()
