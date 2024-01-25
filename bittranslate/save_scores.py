import sys
import csv


def save_scores(step,
                scores,
                uid_score_history,
                uid_score_steps,
                score_logging_file,
                metagraph):
    try:
        used_hotkeys = []
        for uid, score in enumerate(scores):
            hotkey = metagraph.axons[uid].hotkey
            used_hotkeys.append(hotkey)
            if hotkey not in uid_score_history:
                # add history and the recent score
                uid_score_history[hotkey] = [0.0] * step + [score.item()]
            else:
                uid_score_history[hotkey].append(score.item())

        excluded_keys = [hotkey for hotkey in uid_score_history.keys() if hotkey not in used_hotkeys]
        for hotkey in excluded_keys:
            uid_score_history[hotkey].append(0)

        uid_score_steps.append(step)


    except Exception as e:
        print(f"Error saving scores to CSV (noncritical)", file=sys.stderr)
        print(e, file=sys.stderr)

    try:
        with open(score_logging_file, 'w', newline='') as file:
            writer = csv.writer(file)
            write_dict = {"step": uid_score_steps}

            write_dict = {**write_dict, **uid_score_history}
            # Header
            writer.writerow(write_dict.keys())
            # Data
            for row in zip(*write_dict.values()):
                writer.writerow(row)

    except Exception as e:
        print(f"Error writing scores to CSV file (noncritical)", file=sys.stderr)
        print(e, file=sys.stderr)
