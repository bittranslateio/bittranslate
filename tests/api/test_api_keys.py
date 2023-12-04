import argparse
import requests

def ping(port, key):
    try:
        response = requests.post(
            f'http://127.0.0.1:{port}/translate',
            headers={"auth": key},
            json={
                "source_texts": ["input text", "hello world"],
                "source_lang": "en",
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
    result_correct_key = ping(config.port, config.key)
    print("result_correct_key:", result_correct_key)
    assert result_correct_key["detail"] == "success"
    result_wrong_key = ping(config.port, "WRONG KEY")
    print("result_wrong_key:", result_wrong_key)

    assert result_wrong_key["detail"] == "Unauthorized"



if __name__ == "__main__":
    main()