import pandas as pd
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "datasets" / "prepared" / "train_subset.tsv"
OUTPUT_DIR = BASE_DIR / "datasets" / "images_test"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE, sep="\t")

print("Testing image downloads...")
print("Images to test: 20")
print()

success = 0
failed = 0

for index, row in df.head(20).iterrows():

    image_url = row["image_url"]
    image_id = str(row["id"])

    try:
        response = requests.get(
            image_url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200 and len(response.content) > 1000:

            file_path = OUTPUT_DIR / f"{image_id}.jpg"

            with open(file_path, "wb") as f:
                f.write(response.content)

            success += 1
            print(f"[OK] {image_id}")

        else:
            failed += 1
            print(f"[FAILED] {image_id} | HTTP {response.status_code}")

    except Exception as e:
        failed += 1
        print(f"[FAILED] {image_id} | {e}")

print()
print("==============================")
print("IMAGE DOWNLOAD TEST COMPLETE")
print("==============================")
print("Successful:", success)
print("Failed:", failed)