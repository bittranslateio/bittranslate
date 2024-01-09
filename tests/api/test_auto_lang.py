import argparse
import requests

def ping(port, source_text, source_lang):
    try:
        response = requests.post(
            f'http://127.0.0.1:{port}/translate',
            headers={"auth": "change-me"},
            json={
                "source_texts": [source_text],
                "source_lang": source_lang,
                "target_lang": "pl"
            }
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"detail": "error", "translated_texts": []}


def get_config() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8091)
    parser.add_argument("--key", type=str, default="change-me")

    return parser.parse_args()

def main():
    config = get_config()
    source_text_fr = "Quel est ton nom?"

    result_set = ping(config.port, source_text_fr, "fr")
    print("result set:", result_set)

    result_auto = ping(config.port, source_text_fr, "auto")
    print("result auto:", result_auto)

    source_text_ja = "あなたの名前は何ですか"
    result_unsupported_language = ping(config.port, source_text_ja, "auto")
    print("result unsupported:", result_unsupported_language)


if __name__ == "__main__":
    main()