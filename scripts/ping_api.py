import argparse
import requests

def get_config() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8091")
    parser.add_argument("--source_lang", type=str, default="en")
    parser.add_argument("--target_lang", type=str, default="pl")
    parser.add_argument("--source_text", type=str, default="input text")
    parser.add_argument("--auth", type=str, default="change-me")

    return parser.parse_args()

def main():
    config = get_config()
    response = requests.post(
        f'{config.url}/translate',
        headers={"auth": config.auth},
        json={
            "source_texts": [config.source_text],
            "source_lang": config.source_lang,
            "target_lang":  config.target_lang
        }
    )
    print(response.json())

if __name__ == "__main__":
    main()