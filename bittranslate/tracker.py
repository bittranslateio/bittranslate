import json

class Tracker():
    def __init__(self, lang_pairs, n =100):
        self.lang_pairs = lang_pairs
        self.n = n

    @staticmethod
    def _create_lang_pair_key(source_lang: str, target_lang: str) -> str:
        return source_lang + "_" + target_lang

    def _append_to_list(self, l, value):
         if type(value) == float:
             l.append(round(value, 4))
         else:
             l.append(value)

         if len(l) > self.n:
             l.pop(0)



class ValidatorTracker(Tracker):
    def __init__(self, lang_pairs, n=100):
        super().__init__(lang_pairs, n)
        self.score_tracking = {}
        self.text_tracking = {}

        for sublist in lang_pairs:
            lang_pair_key = self._create_lang_pair_key(sublist[0], sublist[1])
            self.score_tracking[lang_pair_key] = {
                "average_scores": list(),
                "max_scores": list(),
                "min_scores": list(),
                "mean": 0,
                "average_max_score": 0,
                "average_min_score": 0
            }

            self.text_tracking[lang_pair_key] = {
                "min": {"sources": list(), "translations": list(), "scores": list()},
                "max": {"sources": list(), "translations": list(), "scores": list()}}

            self.n = n


    def track_scores(self, source_lang, target_lang, scores):

        lang_key = self._create_lang_pair_key(source_lang, target_lang)
        max_score = max(scores)
        min_score = min(scores)

        if len(scores) > 0:
            avg_score = round(sum(scores)/len(scores), 4)
        else:
            avg_score = 0

        score_tracking = self.score_tracking[lang_key]
        averages = score_tracking["average_scores"]
        self._append_to_list(averages, avg_score)

        max_scores = score_tracking["max_scores"]
        self._append_to_list(max_scores, max_score)

        min_scores = score_tracking["min_scores"]
        self._append_to_list(min_scores, min_score)

        score_tracking["mean"] = round(sum(averages)/len(averages), 4)
        score_tracking["average_max_score"] = round(sum(max_scores)/len(max_scores), 4)
        score_tracking["average_min_score"] = round(sum(min_scores)/len(min_scores), 4)

    def track_texts(self, source_lang, target_lang, top_min_source, top_min_target, top_min_score, top_max_source,
                    top_max_target, top_max_score):

        lang_key = self._create_lang_pair_key(source_lang, target_lang)
        tack_lang_pair = self.text_tracking[lang_key]

        tack_lang_pair_min = tack_lang_pair["min"]
        tack_lang_pair_max = tack_lang_pair["max"]

        self._append_to_list(tack_lang_pair_min["sources"], top_min_source)
        self._append_to_list(tack_lang_pair_min["translations"], top_min_target)
        self._append_to_list(tack_lang_pair_min["scores"], top_min_score)

        self._append_to_list(tack_lang_pair_max["sources"], top_max_source)
        self._append_to_list(tack_lang_pair_max["translations"], top_max_target)
        self._append_to_list(tack_lang_pair_max["scores"], top_max_score)

    def scores_to_json(self, output_file: str = "scores_output.json"):
        json_output = json.dumps(self.score_tracking, indent=4)
        with open(output_file, 'w') as file:
            file.write(json_output)

    def texts_to_json(self, output_file: str = "texts_output.json"):
        json_output = json.dumps(self.text_tracking, indent=4)
        with open(output_file, 'w') as file:
            file.write(json_output)

class MiningTracker(Tracker):
    def __init__(self, lang_pairs, n=100):
        super().__init__(lang_pairs, n)

        self.text_tracking = {}

        for sublist in lang_pairs:
            lang_pair_key = self._create_lang_pair_key(sublist[0], sublist[1])
            self.text_tracking[lang_pair_key] = list()


    def track_texts(self, source_lang, target_lang,  source_texts, translated_texts):
        result = {
            "source_texts": source_texts,
            "translated_texts": translated_texts}
        lang_pair_key = self._create_lang_pair_key(source_lang, target_lang)
        self._append_to_list(self.text_tracking[lang_pair_key], result)

    def texts_to_json(self, output_file: str = "texts_output.json"):
        json_output = json.dumps(self.text_tracking, indent=4)
        with open(output_file, 'w') as file:
            file.write(json_output)



