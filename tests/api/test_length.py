import argparse
import requests

def ping(port, key, text, batch_size):
    try:
        response = requests.post(
            f'http://127.0.0.1:{port}/translate',
            headers={"auth": key},
            json={
                "source_texts": [text]*batch_size,
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

    result_normal_length = ping(config.port, config.key, "a"*512, 2)
    print("result_normal_length:", result_normal_length)
    assert result_normal_length["detail"] == "success"

    result_long_text = ping(config.port, config.key, "a" * 513, 2)
    print("result_long_text:", result_long_text)
    assert result_long_text["detail"] == "Source text is too long. Must be under 512 characters"

    result_large_batch_size = ping(config.port, config.key, "a", 3)
    print("result_large_batch_size:", result_large_batch_size)
    assert result_large_batch_size["detail"] == "Batch size for source texts is too large. Please set it to <= 2"


if __name__ == "__main__":
    main()