import argparse
import requests
from concurrent.futures import ThreadPoolExecutor

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

    parser.add_argument("--num_requests", type=int, default=6)
    parser.add_argument("--requests_per_min", type=int, default=4)

    return parser.parse_args()

def main():
    config = get_config()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(ping, config.port, config.key) for _ in range(config.num_requests)]
        results = [future.result() for future in futures]
    for result in results[:config.requests_per_min]:
        assert result["translated_texts"][0] == "Wprowadzenie tekstu"
        assert result["translated_texts"][1] == "Witaj Świat"
    for result in results[config.requests_per_min:]:
        assert result["detail"] == "Rate limit exceeded"
        assert result["detail"] == "Rate limit exceeded"

if __name__ == "__main__":
    main()