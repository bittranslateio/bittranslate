import re
import sys
import os
import random
from typing import List
import numpy as np
from itertools import permutations
from transformers import pipeline
from bittranslate.normalization import sigmoid_normalize, softmax_normalize
from bittranslate.reward_models import BertScore, VectorSim
from bittranslate.prompt_dataset.german_quad import GermanQuAD
from bittranslate.prompt_dataset.exams import Exams
from bittranslate.prompt_dataset.peer_sum import PeerSum
from bittranslate.prompt_dataset.prompt_dataset import PromptDataset
from bittranslate.prompt_dataset.xquad import XQuAD
from bittranslate.prompt_dataset.mkqa import MKqa
from bittranslate.prompt_dataset.bittranslate_dataset import BitTranslateDataset
from bittranslate.tracker import ValidatorTracker
from bittranslate.constants import (TRACKER_HISTORY_COUNT,
                                    SOFTMAX_T_SINGLE,
                                    SOFTMAX_T_FINAL,
                                    MAX_MGPT_PROMPT_LENGTH,
                                    MAX_WENZONG_PROMPT_LENGTH,
                                    MIN_PROMPT_LENGTH,
                                    MAX_PROMPT_LENGTH)
from bittranslate.detect_lang import DetectLang
from bittranslate.util import trim_prompt


class Validator:
    def __init__(self, device: str = "cpu", out_dir: str= "bittranslate_out/" ):
        self._reward_models = [BertScore(device=device), VectorSim(device=device)]

        self._reward_weights = [0.5, 0.5]
        self._mgpt_pipeline = pipeline("text-generation", "ai-forever/mGPT", device=device)

        self._wenzhong_gpt2_pipeline = pipeline("text-generation", "IDEA-CCNL/Wenzhong-GPT2-110M", device=device)

        self._langs =  ["ar", "bg", "de", "el", "en",
                        "es", "et", "fa", "fi", "fr", "hi", "hu", "it", "ko", "pl", "pt",
                        "ro", "ru", "sv", "th",  "tr", "uk", "vi",
                        "zh"]

        self._wenzhong_gpt2_langs = ["zh"]
        self._mgpt_langs = [lang for lang in self._langs if lang not in self._wenzhong_gpt2_langs]

        self._lang_pairs = list(permutations(self._langs, 2))

        self._lang_probs = {
            "en": 0.4,
            "pl": 0.1
        }


        self.tracker = ValidatorTracker(self._lang_pairs, TRACKER_HISTORY_COUNT)

        self.out_dir = out_dir
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        self._detect_lang = DetectLang(output_file=self.out_dir + "lang_detection.json")

        exams = Exams()
        german_quad = GermanQuAD()
        peer_sum = PeerSum()
        xquad = XQuAD()
        mkqa = MKqa()
        bittranslate_dataset = BitTranslateDataset()

        self._datasets = {
                "ar": [xquad],
                "bg": [exams],
                "de": [german_quad, xquad],
                "el": [xquad],
                "en": [peer_sum, xquad],
                "es": [xquad],
                "et": [bittranslate_dataset],
                "fa": [bittranslate_dataset],
                "fi": [bittranslate_dataset],
                "fr": [mkqa, bittranslate_dataset],
                "hi": [xquad],
                "hu": [exams],
                "it": [exams],
                "ko": [bittranslate_dataset],
                "pl": [exams],
                "pt": [exams],
                "ro": [xquad],
                "ru": [xquad],
                "sv": [bittranslate_dataset],
                "th": [xquad],
                "tr": [exams, xquad],
                "uk": [bittranslate_dataset],
                "vi": [exams, xquad],
                "zh": [xquad]}

    def score(self, sources: List[str], translations: List[List[str]], source_lang: str, target_lang: str):
        len_sources = len(sources)
        miners_count = len(translations[0])
        all_scores = [0]*miners_count
        overall_top_max_score = 0
        overall_top_max_source = ""
        overall_top_max_target = ""
        overall_top_min_score = 1.1
        overall_top_min_source = ""
        overall_top_min_target = ""

        top_translations = []
        top_scores = []

        for s, t in zip(sources, translations):
            # s: single source text
            # t: a list of translation where index contains a translation from a given miner.
            # l: target language

            scores = self.single_score(s, t, source_lang, target_lang)
            all_scores = [a + b for a, b in zip(all_scores, scores)]

            max_score = max(scores)
            min_score = min(scores)
            max_score_index = scores.index(max_score)
            min_score_index = scores.index(min_score)
            max_score_value = t[max_score_index]
            top_translations.append(max_score_value)
            top_scores.append(max_score)
            if max_score > overall_top_max_score:
                overall_top_max_score = max_score
                overall_top_max_source = s
                overall_top_max_target = max_score_value

            min_score_value = t[min_score_index]
            if min_score < overall_top_min_score:
                overall_top_min_score = min_score
                overall_top_min_source = s
                overall_top_min_target = min_score_value

        final_scores = [score/len_sources for score in all_scores]
        # Normalize with softmax and scale by number of miners / 2
        final_scores = [score * 0.5 * miners_count for score in softmax_normalize(final_scores, t=SOFTMAX_T_FINAL)]

        # Track scores
        try: # nonessential code:
            self.tracker.track_scores(source_lang, target_lang, final_scores)
        except Exception as e:
            print(f"Error (non-essential code): tracker.log_scores()", file=sys.stderr)
            print(e, file=sys.stderr)

        # Track texts
        try:  # nonessential code:
            self.tracker.track_texts(source_lang, target_lang,
                                     overall_top_min_source,
                                     overall_top_min_target,
                                     overall_top_min_score,
                                     overall_top_max_source,
                                     overall_top_max_target,
                                     overall_top_max_score)
        except Exception as e:
            print(f"Error (non-essential code): tracker.track_texts()", file=sys.stderr)
            print(e, file=sys.stderr)

        return final_scores, top_translations, top_scores

    def single_score(self, source: str, translations: List[str], source_lang: str, target_lang: str) -> List[float]:

        lang_filter = self._filter_lang(translations, source_lang, target_lang)

        reward_scores = [0.0] * len(translations)

        miners_count = len(translations)

        for i, reward_model in enumerate(self._reward_models):
            # Produce scores with a Reward Model
            scores = reward_model.score(source, translations)

            # softmax normalization
            norm_scores = [score * 0.5 * miners_count for score in softmax_normalize(scores, t=SOFTMAX_T_SINGLE)]

            # Get the weight for the Reward Model
            weight = self._reward_weights[i]

            # Multiply each score based on its weight
            weighted_scores = [float(score * weight) for score in norm_scores]

            # Add the resulting weighted scores to the total reward_scores list
            reward_scores = [
                current_score + new_score
                for current_score, new_score in zip(reward_scores, weighted_scores)
            ]

        # Multiply each score by the lang_filter
        # This will zero out any scores that are not in the target language
        result = [a * b for a, b in zip(lang_filter, reward_scores)]

        return result

    def _get_source_dataset(self) -> (PromptDataset, str, str):

        source_lang, target_lang = self._select_lang_pair()

        source_datasets = self._datasets[source_lang]

        random_dataset_index = random.randint(0, len(source_datasets) - 1)
        source_dataset = source_datasets[random_dataset_index]

        return source_dataset, source_lang, target_lang


    def generate_cases(self, count: int=2) -> (str, str, List[str]):
        good_sources = []
        bad_sources = []
        max_iter = count + 4
        curr_iter = 0

        source_dataset, source_lang, target_lang = self._get_source_dataset()

        while len(good_sources) < count and curr_iter < max_iter:
            curr_iter += 1
            starting_case = source_dataset.sample_case(source_lang)
            prompt = self._generate_prompt(starting_case, lang=target_lang)
            if self._is_gibberish(prompt, source_lang):
                bad_sources.append(prompt)
            else:
                good_sources.append(prompt)
        sources = good_sources if len(good_sources) > count else [*good_sources, *bad_sources][:count]
        return source_lang, target_lang, sources

    def _generate_prompt(self, text: str, lang: str = "en") -> str:

        if lang in self._wenzhong_gpt2_langs:
            tokens = self._wenzhong_gpt2_pipeline.tokenizer.encode(text)

            trim_tokens = trim_prompt(tokens, MAX_WENZONG_PROMPT_LENGTH-MAX_PROMPT_LENGTH)

            current_token_length = len(trim_tokens)

            trim_text = self._wenzhong_gpt2_pipeline.tokenizer.decode(trim_tokens)

            return self._wenzhong_gpt2_pipeline(
                trim_text,
                return_full_text=False,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=10,
                temperature=1,
                min_length=MIN_PROMPT_LENGTH + current_token_length,
                max_length=MAX_PROMPT_LENGTH + current_token_length,
            )[0]["generated_text"]
        elif lang in self._mgpt_langs:
            tokens = self._mgpt_pipeline.tokenizer.encode(text)


            trim_tokens = trim_prompt(tokens, MAX_MGPT_PROMPT_LENGTH-MAX_PROMPT_LENGTH)
            current_token_length =  len(trim_tokens)

            trim_text = self._mgpt_pipeline.tokenizer.decode(trim_tokens)


            return self._mgpt_pipeline(
                trim_text,
                return_full_text=False,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=10,
                temperature=1,
                min_length=MIN_PROMPT_LENGTH + current_token_length,
                max_length=MAX_PROMPT_LENGTH + current_token_length,
            )[0]["generated_text"]
        else:
            print("error, language not supported")

    def _filter_lang(self, translations, source_lang, target_lang):
        # Lang detection filter
        lang_filter = []

        for translation in translations:
            try:

                lang_filter_success = self._detect_lang.detect(translation, source_lang, target_lang)

            except Exception as e:
                lang_filter.append(0)
                print(f"Language detection exception. Error {str(e)}. Translation: {translation}", file=sys.stderr)
                continue
            if lang_filter_success:
                lang_filter.append(1)
            else:
                lang_filter.append(0)

        return lang_filter

    def save_tracked_results(self):
        out_scores_path = self.out_dir + "scores.json"
        self.tracker.scores_to_json(out_scores_path)
        out_texts_path = self.out_dir + "texts.json"
        self.tracker.texts_to_json(out_texts_path)

    def _select_lang_pair(self):
        remaining_prob = 1 - sum(self._lang_probs.get(lang, 0) for lang in self._langs)
        langs_wo_prob = [lang for lang in self._langs if lang not in self._lang_probs]
        prob_per_lang = remaining_prob / len(langs_wo_prob)
        probs = {**{lang: prob_per_lang for lang in langs_wo_prob}, **self._lang_probs}
        
        source_lang = np.random.choice(
            self._langs, p=[probs.get(lang) for lang in self._langs]
        ).item()
        target_lang = np.random.choice(
            [lang for lang in self._langs if lang != source_lang]
        ).item()
        return source_lang, target_lang
    
    def _is_gibberish(self, text: str, lang: str) -> bool:
        """
        Filter out gibberish text based on a list of patterns and a cutoff.

        Args:
            text (str): text(prompt) to be filtered
            patterns (List[str]): list of regex patterns to be searched for
            cutoff (float): cutoff for the sum of ratios of pattern matches to text length
        """
        cutoff = 0.2

        chinese_pattern = r'[\u4e00-\u9fff]+'
        emoji_pattern = r'[\U0001F600-\U0001F64F\U00002700-\U000027BF\U0001F680-\U0001F6FF\U00002600-\U000026FF\U0001F900-\U0001F9FF]'
        invalid_pattern = r'[\uE000-\uF8FF]'
        patterns = [emoji_pattern, invalid_pattern]
        if lang != "zh":
            patterns.append(chinese_pattern)
        
        pattern_results = []
        for pattern in patterns:
            chars = "".join(re.findall(pattern, text))
            ratio = round(len(chars)/len(text), 2)
            pattern_results.append(ratio)
        
        if sum(pattern_results) > cutoff:
            return True
        return False