# 🛡️ VERIFAI — Multimodal Misinformation Verification System
### Capstone Project: BAI-12
**Department of Artificial Intelligence | KES' Shroff College**

---

## 📌 Project Overview
VERIFAI is an end-to-end multimodal AI verification engine that detects misinformation and out-of-context multimodal posts across text, images, and live web evidence.

Unlike traditional text-only fact-checkers or unimodal image classifiers, VERIFAI employs:
1. **Multimodal Visual-Language Alignment:** Zero-shot contrastive grounding using **OpenAI CLIP (ViT-B/32)**.
2. **Deep Semantic Image Captioning:** Rich visual description generation via **Salesforce BLIP**.
3. **Multi-Source Evidence Retrieval:** Asynchronous parallel search pulling fact-checks and encyclopedia records across **DuckDuckGo, Wikipedia API, and Fact Check Explorer**.
4. **OCR & Metadata Verification:** Tesseract OCR cross-referencing and EXIF tamper/metadata inspection.
5. **Bayesian/Decision Evidence Fusion:** Calibrated scoring classifying claims as **Likely Consistent (🟢)**, **Potentially Misleading (🔴)**, or **Needs Verification (🟡)**.

---

## 🚀 Quick Start (1-Click Run)

Simply double-click:
```
RUN_VERIFAI.bat
```
This automatically:
- Starts the Flask AI Backend on `http://127.0.0.1:5000`
- Starts the Web Interface on `http://127.0.0.1:5500`
- Launches your default browser to `http://127.0.0.1:5500`

---

## 📁 Project Structure

```
VERIFAI_FINAL/
│
├── RUN_VERIFAI.bat                 <-- 1-Click Master Launcher
├── START_BACKEND.bat               <-- Starts Flask AI server
├── START_FRONTEND.bat              <-- Starts Web UI server
├── README_GUIDE.md                 <-- Full Guide & Viva Preparation
│
├── Backend/                        <-- Python AI Backend
│   ├── app.py                      <-- Flask REST API & Pipeline Orchestrator
│   ├── ai_verifier.py              <-- Contrastive Grounding & Fusion Engine
│   ├── evidence_retrieval.py       <-- Multi-threaded Web Evidence Search
│   ├── ocr.py                      <-- Optical Character Recognition
│   ├── metadata.py                 <-- Image metadata & forensic check
│   ├── trained_model.py            <-- Fakeddit fine-tuned classifier
│   └── requirements.txt            <-- Dependencies list
│
├── Frontend/                       <-- Web Interface
│   ├── index.html                  <-- Modern Responsive UI
│   ├── style.css                   <-- Cyberpunk Glassmorphic Theme
│   └── script.js                   <-- API client with live meter animations
│
└── Test_Images/                    <-- Ready-to-Test Verified Image Suite
    ├── News_Test_Images/           <-- Real & fake news claim images
    │   ├── vande_bharat_train.jpg
    │   ├── taj_mahal_agra.jpg
    │   ├── isro_rocket_launch.jpg
    │   ├── golden_temple_amritsar.jpg
    │   ├── flood_mumbai.jpg
    │   └── shinkansen_train.jpg
    │
    └── Category_Test_Images/       <-- Universal category testing suite
        ├── bmw_car.jpg
        ├── cat_animal.jpg
        ├── apple_fruit.jpg
        ├── pizza_food.jpg
        ├── burj_khalifa_building.jpg
        └── sports_bike.jpg
```

---

## 🧪 Demonstration & Test Cases Table

### 1. Breaking News & Misattribution Benchmark

| Image File (`Test_Images/News_Test_Images/`) | 🟢 Real News Statement | 🔴 Fake / Misleading Statement | Expected Verdict |
|---|---|---|---|
| `vande_bharat_train.jpg` | `Vande Bharat Express semi high speed train running on Indian Railways track` | `Underwater bullet train operating under sea in Dubai desert` | 🟢 Consistent / 🔴 Misleading |
| `taj_mahal_agra.jpg` | `The Taj Mahal white marble mausoleum located in Agra India` | `Royal Buckingham palace situated in London United Kingdom` | 🟢 Consistent / 🔴 Misleading |
| `isro_rocket_launch.jpg` | `ISRO PSLV rocket carrying satellite launching into space from Sriharikota launchpad` | `North Korea testing nuclear intercontinental ballistic missile targeted at Pacific Ocean` | 🟢 Consistent / 🔴 Misleading |
| `golden_temple_amritsar.jpg` | `Golden Temple Sri Harmandir Sahib holy gurdwara in Amritsar Punjab` | `Ancient Buddhist monastery temple located in Kyoto Japan` | 🟢 Consistent / 🔴 Misleading |
| `flood_mumbai.jpg` | `Heavy monsoon rainfall causes waterlogging and flood situation on city streets in Mumbai` | `Catastrophic tsunami flooding in Miami Florida United States` | 🟢 Consistent / 🔴 Misleading |
| `shinkansen_train.jpg` | `High speed Shinkansen bullet train in Japan passing Mount Fuji` | `New bullet train launched in Mumbai India travelling to Ahmedabad` | 🟢 Consistent / 🔴 Misleading |

---

### 2. Universal Object & Category Benchmark

| Image File (`Test_Images/Category_Test_Images/`) | 🟢 Genuine Statement | 🔴 False Statement |
|---|---|---|
| `bmw_car.jpg` | `A luxury BMW sedan car parked outdoors` | `Boeing commercial passenger airplane flying` |
| `cat_animal.jpg` | `A cute domestic cat sitting on the floor` | `A wild tiger in the jungle` |
| `apple_fruit.jpg` | `Fresh red apples on a wooden table` | `A plate of Italian cheese pizza` |
| `pizza_food.jpg` | `Hot oven baked pepperoni cheese pizza` | `A high speed sports motorcycle on highway` |
| `burj_khalifa_building.jpg`| `Burj Khalifa skyscraper building in Dubai` | `An apple fruit hanging on tree branch` |

---

## 🎓 Viva Questions & Key Explanations

1. **Why is Multimodal Verification superior to Text-Only or Image-Only verification?**
   - **Text-Only models fail** when misinformation is phrased politely, formally, or in neutral journalistic language.
   - **Image-Only forensics fail** when the image is 100% authentic (e.g. an authentic 2018 flood photo or Japan train photo) but misattributed to a modern 2026 event or different country.
   - **Multimodal Alignment** compares the semantic compatibility between the visual entities and the textual claim, catching recontextualization.

2. **How does Evidence Retrieval work without rate-limiting?**
   - We query DuckDuckGo, Wikipedia API, and Fact Check Explorer concurrently across background worker threads with polite randomized user-agents and short timeout boundaries, deduplicating records by domain and similarity.

3. **How is the final score calculated?**
   - Visual-Text alignment (CLIP) provides 60% of the weight, BLIP caption overlap contributes 20%, OCR entity match contributes 10%, and metadata contributes 10%. Contradictory evidence or location mismatches penalize the score immediately to protect against hallucinations.
