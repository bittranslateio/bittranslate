import json
import sys
from langdetect import detect
from bittranslate.constants import LANG_PASS_THRESHOLD

class DetectLang():
    def __init__(self, output_file: str):
        self.output_file = output_file

        self.history_lang_detect = {
            'count': 0,
            "fail":{
                'count': 0,
                "source": {},
                "target": {},
                "source-target": {},
                "examples": []
            },
            "pass":{
                'count': 0,
                "source": {},
                "target": {},
                "source-target": {},
                "examples": []
            }
        }


    def detect(self, text, source_lang, target_lang):
        BATCH_SIZES = (8, 16, 32)
        all_words = text.split()
        lang_counts = {}
        for batch_size in BATCH_SIZES:
            for i in range(0, len(all_words), batch_size):
                current_words = all_words[i: i + batch_size]
                joined_words = " ".join(current_words)
                try:
                    lang_detect = detect(joined_words)
                except Exception as e:
                    lang_detect = "error"

                if lang_detect[:2] == "zh":
                    lang_detect= "zh"
                if lang_detect not in lang_counts.keys():
                    # larger batch sizes are worth more
                    lang_counts[lang_detect] = batch_size
                else:
                    lang_counts[lang_detect] += batch_size

        total_count = sum(lang_counts.values())

        if lang_counts:
            top_lang = max(lang_counts, key=lang_counts.get)
        else:
            top_lang = "empty"


        source_lang_count = lang_counts.get(source_lang, 0)
        target_lang_count = lang_counts.get(target_lang, 0)

        if top_lang != target_lang:
            # If target language is not most common, return False.
            success = False

        elif source_lang_count*LANG_PASS_THRESHOLD > target_lang_count:
            # If target language must be much more common than the source language
            success= False
        else:
            success= True

        self.__add_value(success, source_lang, target_lang, text)
        self.__save()

        return success



    def __add_value(self, success: bool, source_lang: str, target_lang: str, text: str):
        self.history_lang_detect["count"]+=1
        sf_string = "pass" if success else "fail"
        self.history_lang_detect[sf_string]["source"][source_lang] = self.history_lang_detect[sf_string][
                                                                         "source"].setdefault(source_lang, 0) + 1
        self.history_lang_detect[sf_string]["target"][target_lang] = self.history_lang_detect[sf_string][
                                                                         "target"].setdefault(target_lang, 0) + 1
        source_target = source_lang + "-" + target_lang
        self.history_lang_detect[sf_string]["source-target"][source_target] = self.history_lang_detect[sf_string][
                                                                           "source-target"].setdefault(source_target,
                                                                                                       0) + 1
        self.history_lang_detect[sf_string]["count"] += 1

        case_dict = {
            "source": source_lang,
            "target": target_lang,
            "text": text
        }
        self.history_lang_detect[sf_string]["examples"].append(case_dict)
        if len(self.history_lang_detect[sf_string]["examples"]) >= 1000:
            self.history_lang_detect[sf_string]["examples"].pop(0)

    def __save(self):
        try:
            with open(self.output_file, 'w') as json_file:
                json.dump(self.history_lang_detect, json_file, indent=2)
        except Exception as e:
            print(f"Error (non-essential code): writing detectLang json: ", e, file=sys.stderr)



        