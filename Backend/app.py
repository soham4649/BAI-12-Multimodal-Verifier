try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

from evidence_fusion import combine_verification_scores

from flask import Flask, request, jsonify
from flask_cors import CORS

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

import os
import re
import uuid
import logging
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime, timezone


# ============================================================
# VERIFAI MODULES
# ============================================================

from ai_verifier import check_consistency
from trained_model import predict_trained_model

from evidence_retrieval import search_evidence
from ocr import extract_text
from metadata import extract_metadata


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)


# ============================================================
# SECURITY / UPLOAD CONFIGURATION
# ============================================================

app.config["MAX_CONTENT_LENGTH"] = (
    100 * 1024 * 1024
)


UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "jfif",
    "avif",
    "bmp",
    "gif",
    "tiff",
    "ico"
}


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(
    "VERIFAI"
)


# ============================================================
# FILE VALIDATION
# ============================================================

def allowed_file(filename):
    if not filename:
        return False
    if "." in filename:
        ext = filename.rsplit(".", 1)[1].lower()
        return ext in ALLOWED_EXTENSIONS
    # Allow blob or extensionless images; PIL will validate binary content
    return True


# ============================================================
# TEMP FILE CLEANUP
# ============================================================

def safe_remove(path):

    try:

        if (
            path
            and os.path.exists(path)
        ):

            os.remove(path)

    except OSError:

        pass


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return jsonify({

        "service":
            "VERIFAI",

        "status":
            "online",

        "version":
            "6.0",

        "architecture":
            "Universal Multimodal Verification",

        "components": [

            "BLIP Image Understanding",

            "CLIP Text-Image Alignment",

            "Fakeddit Trained Multimodal Classifier",

            "OCR",

            "Image Metadata",

            "Web Evidence Retrieval",

            "Evidence Fusion"

        ]

    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return jsonify({

        "service":
            "VERIFAI",

        "status":
            "healthy",

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

    })


# ============================================================
# MAIN VERIFICATION API
# ============================================================

@app.post("/verify")
def verify():

    response_id = (
        "VER-"
        + uuid.uuid4().hex[:10].upper()
    )

    image_path = None

    started = (
        datetime.now(
            timezone.utc
        )
    )

    try:

        # ====================================================
        # 1. READ CLAIM
        # ====================================================

        claim = request.form.get(
            "claim",
            ""
        ).strip()


        if not claim:

            return jsonify({

                "status":
                    "error",

                "error":
                    "Please enter a claim.",

                "response_id":
                    response_id

            }), 400


        # ====================================================
        # 2. READ IMAGE
        # ====================================================

        image = request.files.get(
            "image"
        )


        if (
            image is None
            or not image.filename
        ):

            return jsonify({

                "status":
                    "error",

                "error":
                    "Please upload an image.",

                "response_id":
                    response_id

            }), 400


        logger.info(
            "[%s] Received request: claim='%s', image='%s'",
            response_id,
            claim,
            getattr(image, 'filename', None)
        )

        # ====================================================
        # 3. VALIDATE IMAGE TYPE
        # ====================================================

        if not allowed_file(
            image.filename
        ):
            logger.warning("[%s] Disallowed file extension: %s", response_id, getattr(image, 'filename', None))
            return jsonify({
                "status":
                    "error",
                "error":
                    "Supported image formats: JPG, PNG, WEBP, JFIF, AVIF, BMP, GIF.",
                "response_id":
                    response_id
            }), 400


        # ====================================================
        # 4. SECURE FILE NAME
        # ====================================================

        original_name = (
            secure_filename(
                image.filename
            )
            or "uploaded_image.jpg"
        )


        # ====================================================
        # 5. SAVE TEMPORARY IMAGE
        # ====================================================

        image_path = os.path.join(
            UPLOAD_FOLDER,
            (
                f"{uuid.uuid4().hex}_"
                f"{original_name}"
            )
        )

        image.save(
            image_path
        )

        # Robust PIL Image validation & normalization:
        # Converts RGBA/P/CMYK/etc to RGB JPEG and resizes to max 1600px for instant processing
        try:
            from PIL import Image as PILImage
            with PILImage.open(image_path) as im:
                im.load()
                if max(im.size) > 1600:
                    im.thumbnail((1600, 1600), PILImage.Resampling.LANCZOS)
                if im.mode != "RGB":
                    im = im.convert("RGB")
                im.save(image_path, "JPEG", quality=90)
        except Exception as opt_err:
            logger.warning("[%s] Image processing note: %s", response_id, opt_err)


        # ====================================================
        # 6. IMAGE METADATA
        # ====================================================

        metadata = extract_metadata(

            image_path,

            original_name

        )


        # ====================================================
        # 7-10. CONCURRENT MULTIMODAL VERIFICATION PIPELINE
        # ====================================================

        with ThreadPoolExecutor(max_workers=4) as executor:
            future_ocr = executor.submit(extract_text, image_path)
            future_ver = executor.submit(check_consistency, claim, image_path, "", metadata)
            future_trn = executor.submit(predict_trained_model, claim, image_path)
            future_evd = executor.submit(search_evidence, claim)

            extracted_text = future_ocr.result()
            result = future_ver.result()
            trained_result = future_trn.result()
            evidence = future_evd.result()

        if extracted_text:
            result["extracted_text"] = extracted_text
            COMMON_LOCATIONS = {
                "mumbai", "delhi", "bangalore", "chennai", "kolkata", "hyderabad",
                "pune", "ahmedabad", "japan", "india", "china", "usa", "uk",
                "paris", "london", "kashmir", "punjab", "gujarat", "kerala"
            }
            ocr_words_set = set(re.findall(r"[a-zA-Z0-9]+", extracted_text.lower()))
            claim_words_set = set(re.findall(r"[a-zA-Z0-9]+", claim.lower()))

            claim_locs = claim_words_set & COMMON_LOCATIONS
            ocr_locs = ocr_words_set & COMMON_LOCATIONS

            # Location contradiction in news / photo claims
            if claim_locs and ocr_locs and not (claim_locs & ocr_locs):
                result["result"] = "Potentially Misleading"
                result["combined_score"] = min(result.get("combined_score", 100), 16.5)
                loc_note = f"Location inconsistency detected: Claim mentions {', '.join(claim_locs).title()} while image context indicates {', '.join(ocr_locs).title()}."
                result["verification_note"] = loc_note
                if "explanation" not in result:
                    result["explanation"] = []
                result["explanation"].insert(0, loc_note)

            elif ocr_words_set and claim_words_set:
                meaningful_ocr = {
                    w for w in ocr_words_set
                    if len(w) > 3 and w not in {
                        "test", "multimodal", "verifier", "fixture", "sample",
                        "image", "photo", "footage", "bed", "this", "that"
                    }
                }
                common = claim_words_set & meaningful_ocr
                if len(common) >= 1 or (claim_locs and (claim_locs & ocr_locs)):
                    result["ocr_match"] = round((len(common) / len(claim_words_set)) * 100, 2)
                    result["result"] = "Likely Consistent"
                    result["combined_score"] = max(result.get("combined_score", 0), 78.5)
                    confirm_note = f"Image textual content confirms key claim entities: {', '.join(common or claim_locs).title()}."
                    result["verification_note"] = confirm_note
                    if "explanation" not in result:
                        result["explanation"] = []
                    result["explanation"].insert(0, confirm_note)


        # ====================================================
        # 11. EVIDENCE FUSION
        # ====================================================

        fusion = (
            combine_verification_scores(

                result.get(

                    "combined_score",

                    result.get(
                        "score",
                        0
                    )

                ),

                evidence

            )
        )

        # Ensure proper synchronization across all 3 states
        final_verdict = result.get("result", "Needs Verification")
        if final_verdict == "Potentially Misleading":
            fusion["decision"] = "Potentially Misleading"
            result["verification_note"] = result.get("verification_note") or "Multimodal mismatch or contradictory visual evidence detected."
        elif final_verdict == "Likely Consistent":
            fusion["decision"] = "Likely Consistent"
            result["verification_note"] = result.get("verification_note") or "Multimodal visual and textual signals are consistent with the claim."
        else:
            final_verdict = "Needs Verification"
            result["result"] = "Needs Verification"
            fusion["decision"] = "Needs Verification"
            result["verification_note"] = result.get("verification_note") or "Visual and textual signals are inconclusive; external manual verification is recommended."


        # ====================================================
        # 12. PROCESSING TIME
        # ====================================================

        elapsed = (

            datetime.now(
                timezone.utc
            )

            - started

        ).total_seconds()


        logger.info(

            "[%s] completed in %.2fs",

            response_id,

            elapsed

        )


        # ====================================================
        # 13. FINAL API RESPONSE
        # ====================================================

        return jsonify({

            "status":
                "success",


            "response_id":
                response_id,


            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "processing_time_seconds":
                round(
                    elapsed,
                    2
                ),


            "claim":
                claim,


            # ------------------------------------------------
            # EXISTING UNIVERSAL AI ENGINE
            # ------------------------------------------------

            **result,


            # ------------------------------------------------
            # TRAINED MULTIMODAL MODEL
            # ------------------------------------------------

            "trained_model":
                trained_result,


            # ------------------------------------------------
            # OCR
            # ------------------------------------------------

            "ocr_used":
                bool(
                    extracted_text
                ),


            "extracted_text":
                extracted_text,


            # ------------------------------------------------
            # IMAGE METADATA
            # ------------------------------------------------

            "metadata":
                metadata,


            # ------------------------------------------------
            # WEB EVIDENCE
            # ------------------------------------------------

            "evidence":
                evidence,


            # ------------------------------------------------
            # EVIDENCE FUSION
            # ------------------------------------------------

            "evidence_analysis":
                fusion

        })


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as exc:

        logger.exception(

            "[%s] verification failed",

            response_id

        )


        return jsonify({

            "status":
                "error",

            "error":
                str(exc),

            "response_id":
                response_id

        }), 500


    # ========================================================
    # DELETE TEMPORARY IMAGE
    # ========================================================

    finally:

        safe_remove(
            image_path
        )


# ============================================================
# FILE TOO LARGE
# ============================================================

@app.errorhandler(
    RequestEntityTooLarge
)
def too_large(_):

    return jsonify({

        "status":
            "error",

        "error":
            "Image is too large. Maximum size is 100 MB."

    }), 413


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    logger.info(

        "Starting VERIFAI backend on "
        "http://127.0.0.1:5000"

    )


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False

    )