import torch

from pathlib import Path
from functools import lru_cache
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


# ============================================================
# VERIFAI TRAINED MULTIMODAL MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    BASE_DIR
    / "models"
    / "verifai_multimodal.pt"
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

@lru_cache(maxsize=1)
def load_trained_model():

    if not MODEL_FILE.exists():

        raise FileNotFoundError(
            f"Trained model not found: {MODEL_FILE}"
        )

    checkpoint = torch.load(
        MODEL_FILE,
        map_location=DEVICE
    )

    model_name = checkpoint[
        "clip_model"
    ]

    processor = CLIPProcessor.from_pretrained(
        model_name
    )

    clip_model = CLIPModel.from_pretrained(
        model_name
    )

    clip_model = clip_model.to(
        DEVICE
    )

    clip_model.eval()

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

    return (
        processor,
        clip_model,
        classifier
    )


# ============================================================
# PREDICTION
# ============================================================

def predict_trained_model(
    claim,
    image_path
):
    """
    Runs the trained VERIFAI multimodal classifier.

    Input:
        claim      -> user claim
        image_path -> uploaded image

    Output:
        trained model prediction + confidence
    """

    if not claim:

        raise ValueError(
            "Claim cannot be empty."
        )

    if not image_path:

        raise ValueError(
            "Image path cannot be empty."
        )

    processor, clip_model, classifier = (
        load_trained_model()
    )

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

    except Exception as exc:

        raise ValueError(
            f"Unable to read image: {exc}"
        )


    # --------------------------------------------------------
    # CLIP processing
    # --------------------------------------------------------

    encoded = processor(
        text=str(claim),
        images=image,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=77
    )

    encoded = {
        key: value.to(DEVICE)
        for key, value in encoded.items()
    }


    # --------------------------------------------------------
    # Frozen CLIP embeddings
    # --------------------------------------------------------

    with torch.no_grad():

        outputs = clip_model(
            **encoded
        )

        text_features = (
            outputs.text_embeds
        )

        image_features = (
            outputs.image_embeds
        )

        fused_features = torch.cat(
            [
                text_features,
                image_features
            ],
            dim=1
        )


        # ----------------------------------------------------
        # Trained classifier
        # ----------------------------------------------------

        logits = classifier(
            fused_features
        )

        probabilities = torch.softmax(
            logits,
            dim=1
        )[0]


        predicted_class = int(
            torch.argmax(
                probabilities
            ).item()
        )

        confidence = float(
            probabilities[
                predicted_class
            ].item()
        ) * 100


    # --------------------------------------------------------
    # Class interpretation
    # --------------------------------------------------------

    if predicted_class == 1:

        prediction = "Potentially Misleading"

    else:

        prediction = "Likely Consistent"


    return {

        "prediction": prediction,

        "predicted_class":
            predicted_class,

        "confidence":
            round(confidence, 2),

        "class_0_probability":
            round(
                float(probabilities[0].item()) * 100,
                2
            ),

        "class_1_probability":
            round(
                float(probabilities[1].item()) * 100,
                2
            ),

        "model":
            "VERIFAI Fakeddit Multimodal Classifier"

    }