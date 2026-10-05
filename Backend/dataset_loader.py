import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets"


def load_dataset(split="train"):
    files = {
        "train": "multimodal_train.tsv",
        "validate": "multimodal_validate.tsv",
        "test": "multimodal_test_public.tsv",
    }

    if split not in files:
        raise ValueError("Split must be train, validate or test")

    file_path = DATASET_DIR / files[split]

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    df = pd.read_csv(file_path, sep="\t")

    required_columns = [
        "clean_title",
        "image_url",
        "hasImage",
        "2_way_label",
        "3_way_label",
        "6_way_label",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Only multimodal samples
    df = df[df["hasImage"] == True].copy()

    # Remove rows without text/image URL
    df = df.dropna(subset=["clean_title", "image_url"])

    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    train = load_dataset("train")

    print("VERIFAI DATASET LOADER")
    print("----------------------")
    print("Training samples:", len(train))
    print("Text column: clean_title")
    print("Image column: image_url")
    print("Binary label: 2_way_label")
    print("3-class label: 3_way_label")
    print("6-class label: 6_way_label")
    print()
    print(train[[
        "clean_title",
        "image_url",
        "2_way_label"
    ]].head(3).to_string(index=False))