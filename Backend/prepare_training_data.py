import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = DATASET_DIR / "prepared"

OUTPUT_DIR.mkdir(exist_ok=True)

# Reproducible subset sizes
TRAIN_SAMPLES = 10000
VALIDATE_SAMPLES = 2000
TEST_SAMPLES = 2000
RANDOM_SEED = 42


def prepare_split(filename, output_name, sample_size):
    input_file = DATASET_DIR / filename

    print(f"\nReading: {filename}")

    df = pd.read_csv(input_file, sep="\t")

    # Keep only multimodal rows
    df = df[
        (df["hasImage"] == True)
        & df["clean_title"].notna()
        & df["image_url"].notna()
    ].copy()

    # Remove duplicate posts
    df = df.drop_duplicates(subset=["id"])

    # Reproducible random sample
    sample_size = min(sample_size, len(df))

    df = df.sample(
        n=sample_size,
        random_state=RANDOM_SEED
    ).reset_index(drop=True)

    # Keep only fields needed for training/evaluation
    columns = [
        "id",
        "clean_title",
        "image_url",
        "domain",
        "score",
        "num_comments",
        "upvote_ratio",
        "2_way_label",
        "3_way_label",
        "6_way_label"
    ]

    df = df[columns]

    output_file = OUTPUT_DIR / output_name
    df.to_csv(output_file, sep="\t", index=False)

    print(f"Saved: {output_file}")
    print(f"Samples: {len(df)}")

    return df


if __name__ == "__main__":

    print("===================================")
    print("VERIFAI TRAINING DATA PREPARATION")
    print("===================================")

    train = prepare_split(
        "multimodal_train.tsv",
        "train_subset.tsv",
        TRAIN_SAMPLES
    )

    validate = prepare_split(
        "multimodal_validate.tsv",
        "validate_subset.tsv",
        VALIDATE_SAMPLES
    )

    test = prepare_split(
        "multimodal_test_public.tsv",
        "test_subset.tsv",
        TEST_SAMPLES
    )

    print("\n===================================")
    print("PREPARATION COMPLETE")
    print("===================================")
    print("Train:", len(train))
    print("Validation:", len(validate))
    print("Test:", len(test))
    print("Random seed:", RANDOM_SEED)