from PIL import Image
import os
import mimetypes


def extract_metadata(image_path, original_filename=None):
    """Extract privacy-safe image/file metadata.

    GPS and raw EXIF values are intentionally not exposed.
    """
    stat = os.stat(image_path)
    filename = original_filename or os.path.basename(image_path)

    data = {
        "filename": filename,
        "file_size_kb": round(stat.st_size / 1024, 2),
        "mime_type": mimetypes.guess_type(image_path)[0] or "application/octet-stream",
        "format": None,
        "width": None,
        "height": None,
        "aspect_ratio": None,
        "megapixels": None,
        "mode": None,
        "exif_present": False,
    }

    with Image.open(image_path) as image:
        data["format"] = image.format or "Unknown"
        data["width"] = image.width
        data["height"] = image.height
        data["mode"] = image.mode
        data["aspect_ratio"] = round(image.width / image.height, 3) if image.height else None
        data["megapixels"] = round((image.width * image.height) / 1_000_000, 2)
        data["exif_present"] = bool(image.getexif())

    flags = []
    if data["width"] and data["height"]:
        if min(data["width"], data["height"]) < 480:
            flags.append("Low-resolution image")
        if data["aspect_ratio"] and (data["aspect_ratio"] > 3.5 or data["aspect_ratio"] < 0.28):
            flags.append("Unusual aspect ratio")

    data["quality_flags"] = flags
    data["privacy_note"] = "GPS/raw EXIF values are not exposed."
    return data
