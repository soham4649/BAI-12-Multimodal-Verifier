const claimInput = document.getElementById("claim");
const imageInput = document.getElementById("image");
const imagePreview = document.getElementById("imagePreview");
const uploadContent = document.getElementById("uploadContent");
const resultStatus = document.getElementById("resultStatus");
const resultTitle = document.getElementById("resultTitle");
const statusLabel = document.getElementById("statusLabel");
const consistency = document.getElementById("consistency");
const score = document.getElementById("score");
const ocrMatch = document.getElementById("ocrMatch");
const combinedScore = document.getElementById("combinedScore");
const detectedCategory = document.getElementById("detectedCategory");
const ocrText = document.getElementById("ocrText");
const evidenceList = document.getElementById("evidenceList");
const sourceBadge = document.getElementById("sourceBadge");
const finalResult = document.getElementById("finalResult");

const API_BASE = "http://127.0.0.1:5000";

function fillPreset(type) {
    if (type === 1) {
        claimInput.value = "An open grassy field with electrical power lines and transmission towers under cloudy sky";
    } else if (type === 2) {
        claimInput.value = "Severe snowfall and avalanche in Kashmir blocks Jammu highway";
    } else if (type === 3) {
        claimInput.value = "New dangerous prescription drug pills seized by police at international border";
    }
}

function escapeHTML(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function previewImage() {
    const file = imageInput.files[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) {
        alert("Please select a valid image file.");
        imageInput.value = "";
        return;
    }
    const reader = new FileReader();
    reader.onload = event => {
        imagePreview.src = event.target.result;
        imagePreview.style.display = "block";
        if (uploadContent) uploadContent.style.display = "none";
        imagePreview.classList.remove("preview-pop");
        void imagePreview.offsetWidth;
        imagePreview.classList.add("preview-pop");
    };
    reader.readAsDataURL(file);
}

function wait(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

async function runProcessingAnimation() {
    const resultCard = document.querySelector(".result-card");
    if (!resultCard) return;

    let overlay = resultCard.querySelector(".verifai-processing");
    if (overlay) overlay.remove();

    overlay = document.createElement("div");
    overlay.className = "verifai-processing active";
    overlay.innerHTML = `
        <div class="processing-orbit">
            <div class="orbit-ring ring-one"></div>
            <div class="orbit-ring ring-two"></div>
            <div class="orbit-core">V</div>
        </div>
        <div class="processing-copy">
            <strong id="processingTitle">Reading claim...</strong>
            <span id="processingStep">VERIFAI AI ENGINE</span>
        </div>
        <div class="processing-progress"><span id="processingBar"></span></div>
    `;
    resultCard.appendChild(overlay);

    const title = overlay.querySelector("#processingTitle");
    const step = overlay.querySelector("#processingStep");
    const bar = overlay.querySelector("#processingBar");
    const stages = [
        ["Reading claim...", "TEXT ENCODER", 18],
        ["Understanding image...", "VISION ENCODER", 40],
        ["Checking visual consistency...", "MULTIMODAL FUSION", 62],
        ["Reading image text...", "OCR ANALYSIS", 76],
        ["Retrieving evidence...", "EVIDENCE RETRIEVAL", 90],
        ["Building final verification...", "DECISION ENGINE", 98]
    ];
    for (const [message, label, progress] of stages) {
        title.textContent = message;
        step.textContent = label;
        bar.style.width = `${progress}%`;
        await wait(300);
    }
    overlay.classList.remove("active");
    setTimeout(() => overlay.remove(), 350);
}

function setResultState(type, title, label, iconText = "?") {
    resultStatus.className = `result-status ${type}`;
    resultTitle.innerText = title;
    statusLabel.innerText = label;
    const iconEl = resultStatus.querySelector(".status-icon");
    if (iconEl) iconEl.innerText = iconText;
}

function renderEvidence(evidence) {
    sourceBadge.innerText = `${evidence.length} SOURCES`;
    if (!evidence.length) {
        evidenceList.innerHTML = `
            <div class="empty-state">
                <div>⌕</div>
                <p>No relevant web evidence was retrieved. Human verification is required.</p>
            </div>`;
        return;
    }

    evidenceList.innerHTML = evidence.map(item => `
        <div class="evidence-card">
            <div class="evidence-content">
                <h4>${escapeHTML(item.title || "Source")}</h4>
                <p>${escapeHTML(item.snippet || "No snippet available.")}</p>
                <span class="evidence-relevance">${escapeHTML(item.domain || "source")} · Relevance ${escapeHTML(item.relevance ?? "—")}%</span><br>
                <a href="${escapeHTML(item.link || "#")}" target="_blank" rel="noopener noreferrer">Open Source →</a>
            </div>
        </div>
    `).join("");
}

function renderMetadata(metadata) {
    const box = document.getElementById("metadataContent");
    if (!box || !metadata) return;
    const flags = metadata.quality_flags?.length ? metadata.quality_flags.join(", ") : "No quality flags";
    box.innerHTML = `
        <div class="metadata-grid">
            <div><span>FORMAT</span><strong>${escapeHTML(metadata.format)}</strong></div>
            <div><span>DIMENSIONS</span><strong>${metadata.width} × ${metadata.height}</strong></div>
            <div><span>SIZE</span><strong>${metadata.file_size_kb} KB</strong></div>
            <div><span>ASPECT RATIO</span><strong>${metadata.aspect_ratio}</strong></div>
            <div><span>MEGAPIXELS</span><strong>${metadata.megapixels}</strong></div>
            <div><span>EXIF</span><strong>${metadata.exif_present ? "Present" : "Not exposed"}</strong></div>
        </div>
        <small>${escapeHTML(flags)} · ${escapeHTML(metadata.privacy_note || "Privacy-safe metadata")}</small>
    `;
}

async function verifyClaim() {
    const claim = claimInput.value.trim();
    const image = imageInput.files[0];

    if (!claim) return alert("Please enter a claim or news statement.");
    if (!image) return alert("Please upload an image.");

    setResultState("neutral", "Analyzing...", "AI ANALYSIS IN PROGRESS");
    consistency.innerText = "Analyzing";
    score.innerText = "—";
    ocrMatch.innerText = "—";
    combinedScore.innerText = "—";
    detectedCategory.innerText = "Analyzing";
    ocrText.innerText = "Extracting text...";
    finalResult.innerText = "VERIFAI is analyzing text, image, metadata and evidence.";
    evidenceList.innerHTML = `<div class="empty-state"><div>⌕</div><p>Searching for evidence...</p></div>`;
    sourceBadge.innerText = "SEARCHING";

    const button = document.querySelector(".verify-btn");
    if (button) button.disabled = true;

    const formData = new FormData();
    formData.append("claim", claim);
    formData.append("image", image);

    const animation = runProcessingAnimation();

    try {
        const health = await fetch(`${API_BASE}/health`, { cache: "no-store" });
        if (!health.ok) throw new Error("VERIFAI backend is not healthy. Start Backend/app.py first.");

        const response = await fetch(`${API_BASE}/verify`, {
            method: "POST",
            body: formData
        });

        let data;
        try { data = await response.json(); }
        catch { throw new Error("Backend returned an invalid response. Check the Flask terminal."); }

        if (!response.ok || data.status === "error") {
            throw new Error(data.error || "Verification failed.");
        }

        await animation;

        if (data.result === "Likely Consistent") {
            setResultState("success", data.result, "ANALYSIS COMPLETE", "✓");
        } else if (data.result === "Potentially Misleading") {
            setResultState("danger", data.result, "MISMATCH DETECTED", "✕");
        } else {
            setResultState("neutral", data.result || "Needs Verification", "REVIEW REQUIRED", "?");
        }

        consistency.innerText = `${data.combined_score ?? 0}%`;
        score.innerText = data.score ?? "—";
        ocrMatch.innerText = `${data.ocr_match ?? 0}%`;
        combinedScore.innerText = `${data.combined_score ?? 0}%`;
        detectedCategory.innerText = data.detected_category || "Unknown";
        ocrText.innerText = data.extracted_text || "No text detected.";
        renderEvidence(data.evidence || []);
        renderMetadata(data.metadata);

        const reasons = (data.explanation || []).map(x => `<li>${escapeHTML(x)}</li>`).join("");
        finalResult.innerHTML = `
            <strong>${escapeHTML(data.result)}</strong><br>
            ${escapeHTML(data.verification_note || "Multimodal analysis completed.")}
            <ul class="explanation-list">${reasons}</ul>
            <small>Response ID: ${escapeHTML(data.response_id)} · Processing: ${data.processing_time_seconds}s</small>
        `;
    } catch (error) {
        await animation;
        const errMsg = error.message || "Analysis Error";
        setResultState("danger", errMsg, "VERIFICATION ERROR", "!");
        consistency.innerText = "—";
        score.innerText = "—";
        ocrMatch.innerText = "—";
        combinedScore.innerText = "—";
        detectedCategory.innerText = "Error";
        ocrText.innerText = "—";
        finalResult.innerHTML = `<strong>${escapeHTML(errMsg)}</strong><br><small>Please check the image format or select an image from news_test_images.</small>`;
        sourceBadge.innerText = "0 SOURCES";
        evidenceList.innerHTML = `<div class="empty-state"><div>!</div><p>${escapeHTML(errMsg)}</p></div>`;
    } finally {
        if (button) button.disabled = false;
    }
}

if (imageInput) imageInput.addEventListener("change", previewImage);
if (claimInput) claimInput.addEventListener("keydown", e => {
    if (e.ctrlKey && e.key === "Enter") verifyClaim();
});
