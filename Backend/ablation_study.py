try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

import os
import sys
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from transformers import CLIPProcessor, CLIPModel

# ============================================================
# BAI-12 | MODALITY ABLATION & BASELINE COMPARISON STUDY
# ============================================================
# Compares:
# 1. Text-Only Baseline (CLIP Text features -> Linear Classifier)
# 2. Image-Only Baseline (CLIP Vision features -> Linear Classifier)
# 3. Multimodal Fusion (Text + Image features -> Fused Linear Classifier)
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "datasets" / "prepared" / "train_available.tsv"
IMAGE_DIR = BASE_DIR / "datasets" / "images"
MODEL_FILE = BASE_DIR / "models" / "verifai_multimodal.pt"
OUTPUT_DIR = BASE_DIR / "evaluation_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 70)
print("BAI-12: MODALITY ABLATION STUDY & BASELINE BENCHMARK")
print("=" * 70)
print(f"Device: {DEVICE}")

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset file missing: {DATA_FILE}")

# Load test subset
df = pd.read_csv(DATA_FILE, sep="\t")
print(f"Loaded {len(df)} samples from dataset.")

# Use first 150 available samples for fast & accurate ablation
valid_samples = []
for _, row in df.iterrows():
    img_p = IMAGE_DIR / f"{row['id']}.jpg"
    if img_p.exists():
        valid_samples.append(row)
    if len(valid_samples) >= 150:
        break

eval_df = pd.DataFrame(valid_samples)
print(f"Selected {len(eval_df)} verified image-text pairs for ablation evaluation.")

# Load CLIP
MODEL_NAME = "openai/clip-vit-base-patch32"
print(f"Loading CLIP backbone ({MODEL_NAME})...")
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE)
model.eval()

# Extract representations
text_embeddings = []
image_embeddings = []
labels = []

print("Extracting unimodal and cross-modal embeddings...")
with torch.no_grad():
    for idx, row in eval_df.iterrows():
        img_p = IMAGE_DIR / f"{row['id']}.jpg"
        try:
            img = Image.open(img_p).convert("RGB")
        except Exception:
            continue

        text = str(row["clean_title"])
        encoded = processor(
            text=text,
            images=img,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=77
        )

        input_ids = encoded["input_ids"].to(DEVICE)
        attention_mask = encoded["attention_mask"].to(DEVICE)
        pixel_values = encoded["pixel_values"].to(DEVICE)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            pixel_values=pixel_values
        )

        t_feat = outputs.text_embeds.cpu().numpy()[0]
        i_feat = outputs.image_embeds.cpu().numpy()[0]

        text_embeddings.append(t_feat)
        image_embeddings.append(i_feat)
        labels.append(int(row["2_way_label"]))

X_text = np.array(text_embeddings)
X_img = np.array(image_embeddings)
X_fused = np.concatenate([X_text, X_img], axis=1)
y = np.array(labels)

print(f"Successfully processed {len(y)} samples for ablation.")

# Train/Evaluate Simple Logistic Heads on 80/20 split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_t_train, X_t_test, X_i_train, X_i_test, X_f_train, X_f_test, y_train, y_test = train_test_split(
    X_text, X_img, X_fused, y, test_size=0.25, random_state=42, stratify=y
)

results = []

# 1. Text-Only Baseline
clf_text = LogisticRegression(max_iter=1000, random_state=42)
clf_text.fit(X_t_train, y_train)
y_pred_text = clf_text.predict(X_t_test)
results.append({
    "Configuration": "Text-Only Baseline (CLIP Text)",
    "Accuracy": accuracy_score(y_test, y_pred_text),
    "Macro Precision": precision_score(y_test, y_pred_text, average="macro", zero_division=0),
    "Macro Recall": recall_score(y_test, y_pred_text, average="macro", zero_division=0),
    "Macro F1": f1_score(y_test, y_pred_text, average="macro", zero_division=0)
})

# 2. Image-Only Baseline
clf_img = LogisticRegression(max_iter=1000, random_state=42)
clf_img.fit(X_i_train, y_train)
y_pred_img = clf_img.predict(X_i_test)
results.append({
    "Configuration": "Image-Only Baseline (CLIP Vision)",
    "Accuracy": accuracy_score(y_test, y_pred_img),
    "Macro Precision": precision_score(y_test, y_pred_img, average="macro", zero_division=0),
    "Macro Recall": recall_score(y_test, y_pred_img, average="macro", zero_division=0),
    "Macro F1": f1_score(y_test, y_pred_img, average="macro", zero_division=0)
})

# 3. Multimodal Fusion (Proposed System)
clf_fused = LogisticRegression(max_iter=1000, random_state=42)
clf_fused.fit(X_f_train, y_train)
y_pred_fused = clf_fused.predict(X_f_test)
results.append({
    "Configuration": "Proposed Multimodal Fusion (VERIFAI)",
    "Accuracy": accuracy_score(y_test, y_pred_fused),
    "Macro Precision": precision_score(y_test, y_pred_fused, average="macro", zero_division=0),
    "Macro Recall": recall_score(y_test, y_pred_fused, average="macro", zero_division=0),
    "Macro F1": f1_score(y_test, y_pred_fused, average="macro", zero_division=0)
})

# Convert to DataFrame
res_df = pd.DataFrame(results)

# Save to CSV
csv_path = OUTPUT_DIR / "ablation_study_results.csv"
res_df.to_csv(csv_path, index=False)

print("\n" + "=" * 70)
print("ABLATION STUDY SUMMARY (MANDATORY CAPSTONE METRICS)")
print("=" * 70)
print(res_df.to_string(index=False))
print("=" * 70)
print(f"\nResults successfully exported to: {csv_path}\n")
