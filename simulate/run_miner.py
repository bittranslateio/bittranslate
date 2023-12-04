import argparse
import json
from neurons.miners.m2m_miner import M2MMiner
from mock.mock_network import mocked_network
from neurons.protocol import Translate
from bittranslate import Validator
import time

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rounds",
        type=int,
        default=100,
        help="Number of rounds that will be performed for evaluating the model"
    )
    parser.add_argument('--val_device',
                        default="cuda",
                        help="The device used for the validator's components.")

    parser.add_argument('--save_data',
                        default=None,
                        help="Where the generated data will be saved. If None no saving will occur..")

    parser.add_argument('--load_data',
                        default=None,
                        help="Path to where data will be loaded from. If None new data will be generated.")

    M2MMiner.add_args(parser)
    args = parser.parse_args()
    return args

def main():
    with mocked_network():
        miner = M2MMiner()

    miner.axon.start()
    args = get_config()

    validator = Validator(args.val_device)
    run_times = []
    all_scores = []

    if args.save_data is not None:
        if not args.save_data.endswith(".json"):
            raise ValueError("--save_data does not contain a valid json path")

    loaded_data = {
        "source_langs": [],
        "target_langs": [],
        "source_texts": []}

    if args.load_data is not None:
        if not args.load_data.endswith(".json"):
            raise ValueError("--load_data does not contain a valid json path")
        with open(args.load_data, 'r') as file:
            loaded_data = json.load(file)
        rounds = len(loaded_data["source_texts"])
        if rounds == 0:
            raise ValueError(f"{args.load_data} has no data")

    else:
        rounds = args.rounds

    save_data = {
        "source_langs": [],
        "target_langs": [],
        "source_texts": []}


    for i in range(0, rounds):
        if not args.load_data is not None:
            source_lang, target_lang, source_texts = validator.generate_cases(count=1)
            synapse = Translate(
                        source_texts=source_texts,
                        source_lang=source_lang,
                        target_lang=target_lang)
            if args.save_data is not None:
                save_data["source_langs"].append(source_lang)
                save_data["target_langs"].append(target_lang)
                save_data["source_texts"].append(source_texts)

        else:
            synapse = Translate(
                source_texts=loaded_data["source_texts"][i],
                source_lang=loaded_data["source_langs"][i],
                target_lang=loaded_data["target_langs"][i])
            if args.save_data is not None:
                print("save_data ignored since load_data has been enabled.")


        start = time.time()

        result = miner.forward(synapse)
        end = time.time()

        run_time = end-start

        run_times.append(run_time)

        scores = validator.score(result.source_texts,
                        [result.translated_texts],
                        result.source_lang,
                        result.target_lang)

        all_scores.append(scores[0][0])

        print(f"\n\n\nSource Language: {result.source_lang}", end="\n\n")
        print(f"Target Language: {result.target_lang} ",  end="\n\n")
        print(f"Source: {result.source_texts[0]}",  end="\n\n")
        print(f"Translation: {result.translated_texts[0]}", end="\n\n")
        print("Current time: ", (round(run_time, 3)), "s", end="\n\n")
        print("Current score: ", round(scores[0][0], 3), end="\n\n")

        if i < args.rounds:
            print("Average time: ", (round(sum(run_times) / len(run_times), 3)), "s", end="\n\n")
            print("Average score: ", round(sum(all_scores) / len(all_scores), 3),  end="\n\n")


    if args.save_data is not None:
        print(f"Saving data to: {args.save_data}", end="\n\n")
        with open(args.save_data, 'w') as file:
            json.dump(save_data, file, indent=4)

    print("Final average time: ", round(sum(run_times) / len(run_times), 3), "s", end="\n\n")
    print("Final average score: ", round(sum(all_scores) / len(all_scores), 3), end="\n\n")


if __name__ == "__main__":
    main()
