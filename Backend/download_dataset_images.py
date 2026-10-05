import pandas as pd
import requests
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "datasets" / "prepared"
IMAGE_DIR = BASE_DIR / "datasets" / "images"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

SPLITS = {
    "train": "train_subset.tsv",
    "validate": "validate_subset.tsv",
    "test": "test_subset.tsv",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

MAX_RETRIES = 3
TIMEOUT = 15


def download_image(image_id, image_url):
    output_file = IMAGE_DIR / f"{image_id}.jpg"

    # Already downloaded
    if output_file.exists() and output_file.stat().st_size > 1000:
        return "cached"

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            response = requests.get(
                image_url,
                headers=HEADERS,
                timeout=TIMEOUT
            )

            if response.status_code == 200 and len(response.content) > 1000:

                with open(output_file, "wb") as f:
                    f.write(response.content)

                return "downloaded"

            print(
                f"  Attempt {attempt}: HTTP {response.status_code}"
            )

        except Exception as e:
            print(
                f"  Attempt {attempt}: {type(e).__name__}"
            )

        time.sleep(1)

    return "failed"


def process_split(split_name, filename):

    input_file = DATASET_DIR / filename
    df = pd.read_csv(input_file, sep="\t")

    print()
    print("=" * 45)
    print(f"PROCESSING: {split_name.upper()}")
    print("=" * 45)
    print("Total images:", len(df))

    downloaded = 0
    cached = 0
    failed = 0

    for index, row in df.iterrows():

        image_id = str(row["id"])
        image_url = str(row["image_url"])

        result = download_image(image_id, image_url)

        if result == "downloaded":
            downloaded += 1

        elif result == "cached":
            cached += 1

        else:
            failed += 1

        if (index + 1) % 100 == 0:
            print(
                f"Progress: {index + 1}/{len(df)} | "
                f"Downloaded: {downloaded} | "
                f"Cached: {cached} | "
                f"Failed: {failed}"
            )

    print()
    print(f"{split_name} complete")
    print("Downloaded:", downloaded)
    print("Already cached:", cached)
    print("Failed:", failed)

    return downloaded, cached, failed


if __name__ == "__main__":

    print("========================================")
    print("VERIFAI IMAGE CACHE PIPELINE")
    print("========================================")

    total_downloaded = 0
    total_cached = 0
    total_failed = 0

    for split_name, filename in SPLITS.items():

        downloaded, cached, failed = process_split(
            split_name,
            filename
        )

        total_downloaded += downloaded
        total_cached += cached
        total_failed += failed

    print()
    print("========================================")
    print("IMAGE CACHE PIPELINE COMPLETE")
    print("========================================")
    print("Downloaded:", total_downloaded)
    print("Already cached:", total_cached)
    print("Failed:", total_failed)
    print("Image folder:", IMAGE_DIR)