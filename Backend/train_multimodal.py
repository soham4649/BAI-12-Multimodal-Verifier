import pandas as pd
import torch

from pathlib import Path
from PIL import Image, UnidentifiedImageError
from torch.utils.data import Dataset, DataLoader, default_collate
from transformers import CLIPProcessor, CLIPModel


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "datasets" / "prepared" / "train_available.tsv"
IMAGE_DIR = BASE_DIR / "datasets" / "images"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# SETTINGS
# ============================================================

BATCH_SIZE = 4
EPOCHS = 3
LEARNING_RATE = 2e-4

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 60)
print("VERIFAI BALANCED MULTIMODAL TRAINING")
print("=" * 60)
print("Device:", DEVICE)


# ============================================================
# DATASET
# ============================================================

class FakedditDataset(Dataset):

    def __init__(self, dataframe, processor):

        self.df = dataframe.reset_index(drop=True)
        self.processor = processor

    def __len__(self):

        return len(self.df)

    def __getitem__(self, index):

        row = self.df.iloc[index]

        image_path = IMAGE_DIR / f"{row['id']}.jpg"

        try:

            image = Image.open(image_path).convert("RGB")

        except (
            UnidentifiedImageError,
            OSError,
            FileNotFoundError
        ):

            return None

        text = str(row["clean_title"])

        label = int(row["2_way_label"])

        encoded = self.processor(
            text=text,
            images=image,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=77
        )

        return {
            "input_ids": encoded["input_ids"].squeeze(0),
            "attention_mask": encoded["attention_mask"].squeeze(0),
            "pixel_values": encoded["pixel_values"].squeeze(0),
            "labels": torch.tensor(
                label,
                dtype=torch.long
            )
        }


def safe_collate(batch):

    batch = [
        item for item in batch
        if item is not None
    ]

    if not batch:
        return None

    return default_collate(batch)


# ============================================================
# LOAD DATA
# ============================================================

if not DATA_FILE.exists():

    raise FileNotFoundError(
        f"Training file not found: {DATA_FILE}"
    )


df = pd.read_csv(
    DATA_FILE,
    sep="\t"
)

print()
print("Training samples:", len(df))


# ============================================================
# CLASS BALANCE
# ============================================================

class_counts = df["2_way_label"].value_counts().sort_index()

print()
print("Class distribution:")

for label, count in class_counts.items():

    print(
        f"Class {label}: {count}"
    )


total = len(df)

class_weights = []

for label in range(2):

    count = class_counts.get(
        label,
        1
    )

    weight = total / (2 * count)

    class_weights.append(weight)


class_weights = torch.tensor(
    class_weights,
    dtype=torch.float32
).to(DEVICE)


print()
print("Class weights:")
print(class_weights)


# ============================================================
# LOAD CLIP
# ============================================================

MODEL_NAME = "openai/clip-vit-base-patch32"

print()
print("Loading CLIP model...")

processor = CLIPProcessor.from_pretrained(
    MODEL_NAME
)

model = CLIPModel.from_pretrained(
    MODEL_NAME
)

model = model.to(DEVICE)


# ============================================================
# FREEZE CLIP
# ============================================================

print()
print("Freezing CLIP encoder...")

for parameter in model.parameters():

    parameter.requires_grad = False


model.eval()


# ============================================================
# DATA LOADER
# ============================================================

dataset = FakedditDataset(
    dataframe=df,
    processor=processor
)

loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,
    collate_fn=safe_collate
)


# ============================================================
# MULTIMODAL CLASSIFIER
# ============================================================

feature_size = model.config.projection_dim * 2

classifier = torch.nn.Sequential(

    torch.nn.Linear(
        feature_size,
        256
    ),

    torch.nn.ReLU(),

    torch.nn.Dropout(0.2),

    torch.nn.Linear(
        256,
        2
    )

).to(DEVICE)


# ============================================================
# LOSS + OPTIMIZER
# ============================================================

loss_function = torch.nn.CrossEntropyLoss(
    weight=class_weights
)

optimizer = torch.optim.AdamW(
    classifier.parameters(),
    lr=LEARNING_RATE
)


# ============================================================
# TRAINING
# ============================================================

print()
print("=" * 60)
print("STARTING TRAINING")
print("=" * 60)

classifier.train()

for epoch in range(EPOCHS):

    total_loss = 0.0
    valid_batches = 0

    for step, batch in enumerate(loader):

        if batch is None:
            continue

        input_ids = batch[
            "input_ids"
        ].to(DEVICE)

        attention_mask = batch[
            "attention_mask"
        ].to(DEVICE)

        pixel_values = batch[
            "pixel_values"
        ].to(DEVICE)

        labels = batch[
            "labels"
        ].to(DEVICE)

        optimizer.zero_grad()

        # CLIP is frozen, so no gradients are calculated here.
        with torch.no_grad():

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                pixel_values=pixel_values
            )

            text_features = outputs.text_embeds

            image_features = outputs.image_embeds

            fused_features = torch.cat(
                [
                    text_features,
                    image_features
                ],
                dim=1
            )

        logits = classifier(
            fused_features
        )

        loss = loss_function(
            logits,
            labels
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

        valid_batches += 1

        if (step + 1) % 25 == 0:

            print(
                f"Epoch {epoch + 1}/{EPOCHS} | "
                f"Step {step + 1}/{len(loader)} | "
                f"Loss: {loss.item():.4f}"
            )

    average_loss = (
        total_loss / valid_batches
        if valid_batches > 0
        else 0.0
    )

    print()
    print(
        f"Epoch {epoch + 1} complete | "
        f"Average Loss: {average_loss:.4f}"
    )
    print()


# ============================================================
# SAVE CHECKPOINT
# ============================================================

checkpoint_path = (
    MODEL_DIR / "verifai_multimodal.pt"
)

torch.save(
    {
        "clip_model": MODEL_NAME,

        "classifier_state_dict":
            classifier.state_dict(),

        "classifier_input_size":
            feature_size,

        "num_classes": 2,

        "class_weights":
            class_weights.cpu(),

        "epochs": EPOCHS,

        "learning_rate":
            LEARNING_RATE,

        "training_samples":
            len(df),

        "clip_frozen": True
    },
    checkpoint_path
)


# ============================================================
# DONE
# ============================================================

print("=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print()
print("Model saved at:")

print(checkpoint_path)

print()
print("The CLIP encoder was frozen.")
print("The multimodal classifier was trained.")
print("Class-balanced loss was used.")