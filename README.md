# VERIFAI — Multimodal Misinformation Verification

A capstone prototype for checking whether a claim is consistent with an uploaded image using:

- CLIP text-image analysis
- visual category detection
- vehicle/entity consistency checks
- OCR with EasyOCR
- privacy-safe image metadata features
- evidence retrieval
- explanation of the final decision
- response IDs and processing logs
- security limits and input validation

## Demo cases

1. BMW image + `This is a BMW car.` → expected consistent signal.
2. Tata Punch image + `This is a BMW car.` → expected mismatch / potentially misleading signal.
3. Mountain image + `This is a car.` → expected category mismatch.
4. News/document screenshot + matching claim → OCR + evidence workflow.

## Run backend

Open PowerShell inside `Backend`:

```powershell
pip install -r requirements.txt
python app.py
```

Check:

`http://127.0.0.1:5000/health`

It should return JSON with `status: healthy`.

## Run frontend

Open `Frontend/index.html` in a browser, or serve the folder with:

```powershell
python -m http.server 5500
```

Then open `http://127.0.0.1:5500`.

## Important model note

The vehicle/entity module is a zero-shot CLIP-based consistency layer. It is intended as an AI-assisted signal, not as a certified vehicle identification system. The UI therefore reports a verification signal and explanation rather than claiming ground-truth identity.

## Privacy

Raw EXIF/GPS values are not exposed. Only safe metadata such as dimensions, format, file size, aspect ratio and whether EXIF exists are returned.
