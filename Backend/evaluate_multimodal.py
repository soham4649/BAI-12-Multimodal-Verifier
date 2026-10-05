import torch
import pandas as pd

from pathlib import Path
from PIL import Image
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from transformers import CLIPProcessor, CLIPModel


# ============================================================
# VERIFAI — FINAL MULTIMODAL EVALUATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "datasets"
    / "prepared"
    / "train_available.tsv"
)

IMAGE_DIR = (
    BASE_DIR
    / "datasets"
    / "images"
)

MODEL_FILE = (
    BASE_DIR
    / "models"
    / "verifai_multimodal.pt"
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


print("=" * 60)
print("VERIFAI MULTIMODAL MODEL EVALUATION")
print("=" * 60)
print("Device:", DEVICE)


# ============================================================
# CHECK FILES
# ============================================================

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

if not MODEL_FILE.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_FILE}"
    )


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    DATA_FILE,
    sep="\t"
)

print("Total samples:", len(df))


# ============================================================
# LOAD CHECKPOINT
# ============================================================

checkpoint = torch.load(
    MODEL_FILE,
    map_location=DEVICE
)

print("Checkpoint loaded successfully.")


# ============================================================
# LOAD CLIP
# ============================================================

MODEL_NAME = checkpoint["clip_model"]

processor = CLIPProcessor.from_pretrained(
    MODEL_NAME
)

model = CLIPModel.from_pretrained(
    MODEL_NAME
)

model = model.to(DEVICE)

model.eval()


# ============================================================
# RECREATE FINAL CLASSIFIER
# ============================================================

input_size = checkpoint[
    "classifier_input_size"
]

num_classes = checkpoint[
    "num_classes"
]


classifier = torch.nn.Sequential(

    torch.nn.Linear(
        input_size,
        256
    ),

    torch.nn.ReLU(),

    torch.nn.Dropout(
        0.2
    ),

    torch.nn.Linear(
        256,
        num_classes
    )

).to(DEVICE)


classifier.load_state_dict(
    checkpoint[
        "classifier_state_dict"
    ]
)

classifier.eval()


# ============================================================
# INFORMATION
# ============================================================

print()
print("Model information:")
print("Training samples:", checkpoint.get(
    "training_samples",
    "N/A"
))

print("Epochs:", checkpoint.get(
    "epochs",
    "N/A"
))

print("CLIP frozen:", checkpoint.get(
    "clip_frozen",
    "N/A"
))

print()


# ============================================================
# EVALUATION
# ============================================================

y_true = []
y_pred = []

processed = 0
skipped = 0


print("=" * 60)
print("RUNNING EVALUATION")
print("=" * 60)
print()


with torch.no_grad():

    for _, row in df.iterrows():

        image_path = (
            IMAGE_DIR
            / f"{row['id']}.jpg"
        )

        # Missing image
        if not image_path.exists():

            skipped += 1
            continue

        # Open image
        try:

            image = Image.open(
                image_path
            ).convert("RGB")

        except Exception:

            skipped += 1
            continue


        # Text
        text = str(
            row["clean_title"]
        )


        # CLIP processor
        encoded = processor(
            text=text,
            images=image,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=77
        )


        input_ids = (
            encoded["input_ids"]
            .to(DEVICE)
        )

        attention_mask = (
            encoded["attention_mask"]
            .to(DEVICE)
        )

        pixel_values = (
            encoded["pixel_values"]
            .to(DEVICE)
        )


        # CLIP embeddings
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            pixel_values=pixel_values
        )


        text_features = (
            outputs.text_embeds
        )

        image_features = (
            outputs.image_embeds
        )


        # Multimodal fusion
        fused_features = torch.cat(
            [
                text_features,
                image_features
            ],
            dim=1
        )


        # Classifier prediction
        logits = classifier(
            fused_features
        )


        prediction = torch.argmax(
            logits,
            dim=1
        ).item()


        actual = int(
            row["2_way_label"]
        )


        y_true.append(actual)
        y_pred.append(prediction)

        processed += 1


        if processed % 100 == 0:

            print(
                f"Evaluated: {processed} samples"
            )


# ============================================================
# SAFETY CHECK
# ============================================================

if len(y_true) == 0:

    raise RuntimeError(
        "No valid samples were available for evaluation."
    )


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0
)

macro_f1 = f1_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0
)

matrix = confusion_matrix(
    y_true,
    y_pred
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 60)
print("FINAL EVALUATION RESULTS")
print("=" * 60)

print(
    f"Samples evaluated : {len(y_true)}"
)

print(
    f"Samples skipped   : {skipped}"
)

print(
    f"Accuracy          : {accuracy:.4f}"
)

print(
    f"Macro Precision   : {precision:.4f}"
)

print(
    f"Macro Recall      : {recall:.4f}"
)

print(
    f"Macro F1          : {macro_f1:.4f}"
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print()
print("Confusion Matrix:")

print(matrix)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print()
print("Classification Report:")

print(
    classification_report(
        y_true,
        y_pred,
        target_names=[
            "Class 0",
            "Class 1"
        ],
        zero_division=0
    )
)


# ============================================================
# END
# ============================================================

print()
print("=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)