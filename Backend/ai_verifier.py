try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

import re
from functools import lru_cache

import torch
from PIL import Image
from transformers import (
    CLIPProcessor,
    CLIPModel,
    BlipProcessor,
    BlipForConditionalGeneration
)


# ============================================================
# VERIFAI - FINAL UNIVERSAL MULTIMODAL VERIFICATION ENGINE
# ============================================================
#
# Pipeline:
#
# Claim
#   ↓
# Universal Image Captioning
#   ↓
# CLIP Visual-Text Alignment
#   ↓
# OCR
#   ↓
# Metadata Quality
#   ↓
# Evidence Retrieval happens in app.py
#   ↓
# Evidence Fusion
#   ↓
# Final Verification Decision
#
# This version does NOT depend on a fixed list of:
# dog / car / pizza / Eiffel Tower etc.
#
# ============================================================


CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

# Universal image captioning model
BLIP_MODEL_NAME = "Salesforce/blip-image-captioning-base"


# ============================================================
# DEVICE
# ============================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ============================================================
# MODEL LOADING
# ============================================================

@lru_cache(maxsize=1)
def load_clip():
    """
    Loads CLIP once and reuses it.
    """

    processor = CLIPProcessor.from_pretrained(
        CLIP_MODEL_NAME
    )

    model = CLIPModel.from_pretrained(
        CLIP_MODEL_NAME
    )

    model.to(DEVICE)
    model.eval()

    return processor, model


@lru_cache(maxsize=1)
def load_blip():
    """
    Loads BLIP once and reuses it.

    BLIP creates a natural-language description
    of the uploaded image.
    """

    processor = BlipProcessor.from_pretrained(
        BLIP_MODEL_NAME
    )

    model = BlipForConditionalGeneration.from_pretrained(
        BLIP_MODEL_NAME
    )

    model.to(DEVICE)
    model.eval()

    return processor, model


# ============================================================
# BASIC UTILITIES
# ============================================================

def clean_text(text):
    return re.sub(
        r"\s+",
        " ",
        (text or "").strip().lower()
    )


def tokenize(text):
    """
    Basic tokenization used for lightweight
    claim/caption comparison.
    """

    return set(
        re.findall(
            r"[a-zA-Z0-9]+",
            clean_text(text)
        )
    )


# ============================================================
# IMAGE VALIDATION
# ============================================================

def load_image(image_path):
    """
    Safely loads an image as RGB.
    """

    try:
        image = Image.open(image_path)
        image = image.convert("RGB")
        return image

    except Exception as exc:
        raise ValueError(
            f"Unable to read image: {exc}"
        )


# ============================================================
# UNIVERSAL IMAGE CAPTIONING
# ============================================================

def generate_image_caption(image_path):
    """
    Generates a natural-language description
    of the uploaded image.

    Unlike the old category system, this does not
    require a predefined entity list.
    """

    processor, model = load_blip()

    image = load_image(image_path)

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=35,
            num_beams=1
        )

    caption = processor.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    caption = caption.strip()

    if not caption:
        caption = "No reliable visual description generated."

    return caption


# ============================================================
# CLIP IMAGE <-> TEXT SIMILARITY
# ============================================================

def clip_image_text_similarity(
    image_path,
    text
):
    """
    Contrastive CLIP verification:
    Measures how strongly the image matches the claim vs something completely different.
    Returns calibrated 0-100 probability.
    """

    if not text:
        return 0.0

    processor, model = load_clip()
    image = load_image(image_path)

    clean_t = re.sub(r'^(this\s+(image|photo|picture)\s+(shows|depicts|is)\s+)', '', text.strip(), flags=re.I).strip() or text.strip()

    prompts = [
        f"a photo showing {clean_t}",
        f"a photo that does not show {clean_t}",
        "a photo of something completely different"
    ]

    inputs = processor(
        text=prompts,
        images=image,
        return_tensors="pt",
        padding=True
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)[0]
    match_score = float(probs[0].item()) * 100.0

    return round(max(0.0, min(100.0, match_score)), 2)


# ============================================================
# CLIP TEXT EMBEDDINGS
# ============================================================

def get_text_embedding(text):
    """
    Creates a normalized CLIP text embedding.
    Compatible with Transformers 5.x.
    """

    processor, model = load_clip()

    inputs = processor(
        text=[text],
        return_tensors="pt",
        padding=True
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        if hasattr(model, "get_text_features"):
            feat = model.get_text_features(**inputs)
            if hasattr(feat, "pooler_output") and feat.pooler_output is not None:
                features = feat.pooler_output
            elif hasattr(feat, "text_embeds") and feat.text_embeds is not None:
                features = feat.text_embeds
            else:
                features = feat
        else:
            outputs = model(**inputs)
            features = outputs.text_embeds

    features = features / features.norm(
        dim=-1,
        keepdim=True
    )

    return features


def text_similarity(text_a, text_b):
    """
    Semantic similarity between two text descriptions.
    """

    if not text_a or not text_b:
        return 0.0

    embedding_a = get_text_embedding(text_a)
    embedding_b = get_text_embedding(text_b)

    similarity = torch.cosine_similarity(
        embedding_a,
        embedding_b
    ).item()

    # Convert cosine similarity approximately
    # from [-1, 1] to [0, 100].
    score = ((similarity + 1.0) / 2.0) * 100.0

    return round(
        max(0.0, min(100.0, score)),
        2
    )


STOP_WORDS = {
    'a', 'an', 'the', 'this', 'that', 'is', 'are', 'was', 'were',
    'in', 'on', 'at', 'of', 'for', 'with', 'and', 'to', 'shows',
    'photo', 'image', 'picture', 'depicts', 'there', 'it', 'about'
}

def stem_word(w):
    return re.sub(r'(s|es|ing|ed)$', '', (w or '').lower())

def extract_content_words(text):
    words = re.findall(r'[a-zA-Z0-9]+', (text or '').lower())
    return {
        stem_word(w) for w in words
        if len(w) > 2 and w not in STOP_WORDS
    }

def calculate_word_overlap(
    claim,
    caption
):
    """
    Stemmed lexical overlap of meaningful entity words.
    Filters out common stop words so 'a', 'the', etc. do not cause false matches.
    """
    claim_words = extract_content_words(claim)
    caption_words = extract_content_words(caption)

    if not claim_words:
        return 0.0

    common_words = claim_words.intersection(caption_words)

    return round(
        (len(common_words) / len(claim_words)) * 100.0,
        2
    )


# ============================================================
# OCR MATCH
# ============================================================

def calculate_ocr_match(
    claim,
    extracted_text
):
    """
    Checks whether words from the claim
    appear in text detected inside the image.
    """

    if not extracted_text:
        return 0.0

    claim_words = tokenize(claim)
    ocr_words = tokenize(extracted_text)

    if not claim_words:
        return 0.0

    common_words = claim_words.intersection(
        ocr_words
    )

    return round(
        (len(common_words) / len(claim_words))
        * 100,
        2
    )


# ============================================================
# METADATA QUALITY
# ============================================================

def metadata_quality(metadata):
    """
    Metadata is used as a quality/context signal,
    NOT as proof that an image is genuine.
    """

    if not metadata:
        return 70.0

    score = 100.0

    width = metadata.get(
        "width",
        1000
    )

    height = metadata.get(
        "height",
        1000
    )

    file_size = metadata.get(
        "file_size_kb",
        100
    )

    try:
        width = float(width)
        height = float(height)
        file_size = float(file_size)
    except (
        TypeError,
        ValueError
    ):
        return 70.0

    if width < 300:
        score -= 20

    if height < 300:
        score -= 20

    if file_size < 20:
        score -= 10

    return round(
        max(0.0, min(100.0, score)),
        2
    )


# ============================================================
# CLAIM TYPE SIGNAL
# ============================================================

def detect_claim_characteristics(claim):
    """
    Identifies broad characteristics of a claim.

    This is deliberately generic and does not use
    a fixed entity database.
    """

    text = clean_text(claim)

    characteristics = {
        "has_number": bool(
            re.search(r"\b\d+(?:\.\d+)?\b", text)
        ),

        "has_date": bool(
            re.search(
                r"\b(?:19|20)\d{2}\b",
                text
            )
        ),

        "has_location_language": any(
            word in text.split()
            for word in [
                "in",
                "at",
                "near",
                "from",
                "located"
            ]
        ),

        "has_time_language": any(
            word in text.split()
            for word in [
                "today",
                "yesterday",
                "tomorrow",
                "now",
                "recently",
                "latest"
            ]
        ),

        "has_identity_language": any(
            phrase in text
            for phrase in [
                "is ",
                "called ",
                "named ",
                "this is "
            ]
        )
    }

    return characteristics


# ============================================================
# VISUAL CONTRADICTION & GROUNDED ALIGNMENT
# ============================================================

def calculate_visual_contradiction(
    claim,
    image_path,
    caption
):
    """
    Dual-layer contrastive alignment:
    1. Grounded comparison: Image Content (caption) vs Claim vs Diff
    2. Direct negation contrast: Claim vs Not Claim vs Diff
    """
    if not claim:
        return {
            "match": 0.0,
            "grounded_match": 0.0,
            "contradiction": 0.0,
            "caption_similarity": 0.0
        }

    processor, model = load_clip()
    image = load_image(image_path)

    clean_c = re.sub(r'^(this\s+(image|photo|picture)\s+(shows|depicts|is)\s+)', '', claim.strip(), flags=re.I).strip() or claim.strip()

    # 1. Grounded Contrast: Photo of Caption vs Photo of Claim
    grounded_prompts = [
        f"a photo of {caption}",
        f"a photo showing {clean_c}",
        "a photo of something completely different"
    ]
    inputs_grnd = processor(
        text=grounded_prompts,
        images=image,
        return_tensors="pt",
        padding=True
    )
    inputs_grnd = {k: v.to(DEVICE) for k, v in inputs_grnd.items()}
    with torch.inference_mode():
        out_grnd = model(**inputs_grnd)
    probs_grnd = out_grnd.logits_per_image.softmax(dim=1)[0]
    grounded_claim_prob = float(probs_grnd[1].item()) * 100.0

    # 2. Direct Negation Contrast
    direct_prompts = [
        f"a photo showing {clean_c}",
        f"a photo that does not show {clean_c}",
        "a photo of something completely different"
    ]
    inputs_dir = processor(
        text=direct_prompts,
        images=image,
        return_tensors="pt",
        padding=True
    )
    inputs_dir = {k: v.to(DEVICE) for k, v in inputs_dir.items()}
    with torch.inference_mode():
        out_dir = model(**inputs_dir)
    probs_dir = out_dir.logits_per_image.softmax(dim=1)[0]
    direct_match_prob = float(probs_dir[0].item()) * 100.0
    direct_contra_prob = float((probs_dir[1].item() + probs_dir[2].item())) * 100.0

    caption_similarity = text_similarity(clean_c, caption)

    return {
        "match": round(direct_match_prob, 2),
        "grounded_match": round(grounded_claim_prob, 2),
        "contradiction": round(direct_contra_prob, 2),
        "caption_similarity": round(caption_similarity, 2)
    }


# ============================================================
# FINAL VISUAL SIGNAL
# ============================================================

def calculate_visual_signal(
    claim,
    image_path,
    caption
):
    """
    Combines grounded and direct visual signals.
    """
    contradiction_data = calculate_visual_contradiction(
        claim,
        image_path,
        caption
    )

    direct_match = contradiction_data["match"]
    grounded_match = contradiction_data["grounded_match"]
    caption_similarity = contradiction_data["caption_similarity"]
    contradiction_score = contradiction_data["contradiction"]

    return {
        "visual_signal": round(direct_match, 2),
        "clip_match": round(direct_match, 2),
        "grounded_match": round(grounded_match, 2),
        "caption_similarity": round(caption_similarity, 2),
        "contradiction_signal": round(contradiction_score, 2)
    }


# ============================================================
# DECISION ENGINE
# ============================================================

def make_decision(
    grounded_match,
    direct_match,
    contradiction_signal,
    caption_similarity,
    word_overlap,
    ocr_match=0.0
):
    """
    Universal Multimodal Decision Engine validated across:
    Objects, Buildings, Cars, Bikes, Animals, Fruits, Foods, etc.
    """
    # 1. Undeniable Fake / Misleading:
    # Grounded claim probability is near-zero (< 8%) AND no stemmed entity overlap
    if (grounded_match < 8.0 and word_overlap == 0.0 and caption_similarity < 93.0) or \
       (contradiction_signal >= 80.0 and word_overlap == 0.0 and direct_match < 20.0):
        return ("Potentially Misleading", "High")

    # 2. Consistent / Genuine:
    if (grounded_match >= 15.0 or direct_match >= 40.0) or \
       (word_overlap > 0.0 and caption_similarity >= 85.0) or \
       (ocr_match >= 50.0):
        return ("Likely Consistent", "High")

    # 3. Needs Verification: Inconclusive
    return ("Needs Verification", "Medium")


# ============================================================
# MAIN VERIFICATION FUNCTION
# ============================================================

def check_consistency(
    claim,
    image_path,
    extracted_text="",
    metadata=None
):
    """
    Main VERIFAI verification pipeline.

    Compatible with current app.py:

        check_consistency(
            claim,
            image_path,
            extracted_text,
            metadata
        )
    """

    claim = (
        claim or ""
    ).strip()

    if not claim:
        raise ValueError(
            "Claim cannot be empty."
        )

    # --------------------------------------------------------
    # 1. UNIVERSAL IMAGE UNDERSTANDING
    # --------------------------------------------------------

    image_caption = generate_image_caption(
        image_path
    )

    # --------------------------------------------------------
    # 2. VISUAL-TEXT ANALYSIS
    # --------------------------------------------------------

    visual_data = calculate_visual_signal(
        claim,
        image_path,
        image_caption
    )

    visual_signal = visual_data[
        "visual_signal"
    ]

    # --------------------------------------------------------
    # 3. OCR
    # --------------------------------------------------------

    ocr_match = calculate_ocr_match(
        claim,
        extracted_text
    )

    # --------------------------------------------------------
    # 4. CAPTION WORD OVERLAP
    # --------------------------------------------------------

    word_overlap = calculate_word_overlap(
        claim,
        image_caption
    )

    # --------------------------------------------------------
    # 5. METADATA
    # --------------------------------------------------------

    metadata_score = metadata_quality(
        metadata
    )

    # --------------------------------------------------------
    # 6. CLAIM CHARACTERISTICS
    # --------------------------------------------------------

    claim_characteristics = (
        detect_claim_characteristics(
            claim
        )
    )

    # --------------------------------------------------------
    # 7. CONSISTENCY SIGNAL
    # --------------------------------------------------------

    multimodal_score = (
        visual_signal * 0.60
        + visual_data["caption_similarity"] * 0.20
        + ocr_match * 0.10
        + metadata_score * 0.10
    )

    multimodal_score = max(
        0.0,
        min(100.0, multimodal_score)
    )

    # --------------------------------------------------------
    # 8. CONSERVATIVE INITIAL DECISION
    # --------------------------------------------------------

    result, level = make_decision(
        grounded_match=visual_data.get("grounded_match", 0.0),
        direct_match=visual_signal,
        contradiction_signal=visual_data.get("contradiction_signal", 0.0),
        caption_similarity=visual_data.get("caption_similarity", 0.0),
        word_overlap=word_overlap,
        ocr_match=ocr_match
    )

    if result == "Potentially Misleading":
        multimodal_score = min(
            multimodal_score,
            round(visual_data.get("grounded_match", 0.0) * 0.4 + visual_signal * 0.2 + 10.0, 2)
        )
    elif result == "Likely Consistent":
        multimodal_score = max(multimodal_score, 75.0)

    # --------------------------------------------------------
    # 9. EXPLANATION
    # --------------------------------------------------------

    explanation = []

    explanation.append(
        "AI-generated image description: "
        f"{image_caption}"
    )

    if visual_signal >= 60:
        explanation.append(
            "The visual content shows reasonable "
            "semantic consistency with the claim."
        )

    elif visual_signal < 35:
        explanation.append(
            "The visual content provides weak "
            "semantic support for the claim."
        )

    else:
        explanation.append(
            "The visual content provides moderate "
            "semantic support for the claim."
        )

    if (
        visual_data["contradiction_signal"]
        >= 45
    ):
        explanation.append(
            "The visual-language model also detected "
            "a possible contradiction signal."
        )

    if ocr_match > 0:
        explanation.append(
            f"Image text overlap with the claim: "
            f"{ocr_match:.2f}%."
        )
    else:
        explanation.append(
            "No meaningful claim overlap was found "
            "in detected image text."
        )

    if word_overlap > 0:
        explanation.append(
            f"Caption/claim word overlap: "
            f"{word_overlap:.2f}%."
        )

    # --------------------------------------------------------
    # 10. VERIFICATION NOTE
    # --------------------------------------------------------

    if result == "Likely Consistent":

        verification_note = (
            "The available multimodal signals and "
            "retrieved evidence support the claim, "
            "but external factual verification should "
            "still be considered for high-stakes claims."
        )

    elif result == "Potentially Misleading":

        verification_note = (
            "The image and claim show substantial "
            "semantic inconsistency."
        )

    else:

        verification_note = (
            "The available visual and textual signals "
            "are insufficient for a definitive factual "
            "verification."
        )

    # --------------------------------------------------------
    # 11. FINAL RESPONSE
    # --------------------------------------------------------

    return {

        # Main result
        "result": result,

        "score": round(
            visual_signal,
            2
        ),

        "level": level,

        # Universal image understanding
        "image_caption": image_caption,

        # Visual signals
        "visual_signal": round(
            visual_signal,
            2
        ),

        "clip_match": round(
            visual_data["clip_match"],
            2
        ),

        "caption_similarity": round(
            visual_data[
                "caption_similarity"
            ],
            2
        ),

        "contradiction_signal": round(
            visual_data[
                "contradiction_signal"
            ],
            2
        ),

        # OCR
        "ocr_match": round(
            ocr_match,
            2
        ),

        # Caption lexical support
        "caption_word_overlap": round(
            word_overlap,
            2
        ),

        # Multimodal score
        "combined_score": round(
            multimodal_score,
            2
        ),

        # Metadata
        "metadata_quality": round(
            metadata_score,
            2
        ),

        # Claim information
        "claim_characteristics":
            claim_characteristics,

        # Compatibility fields
        # kept so the existing frontend does
        # not break.
        "detected_category": (
            "Universal Visual Content"
        ),

        "category_confidence": round(
            visual_signal,
            2
        ),

        "claim_category": None,

        "claim_entity": None,

        "detected_entity": None,

        "entity_confidence": 0.0,

        "entity_match": None,

        "identity_supported": False,

        # Explanation
        "explanation": explanation,

        "verification_note":
            verification_note
    }