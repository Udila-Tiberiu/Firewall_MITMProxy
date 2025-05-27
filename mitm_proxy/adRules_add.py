import requests

EASYLIST_URL = "https://easylist.to/easylist/easylist.txt"
OUTPUT_FILE = "../ad_rules.log"

def download_easylist(url: str, output_path: str):
    try:
        print(f"Downloading EasyList from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"EasyList saved to: {output_path}")
    except requests.RequestException as e:
        print(f"Failed to download EasyList: {e}")

if __name__ == "__main__":
    download_easylist(EASYLIST_URL, OUTPUT_FILE)
