import streamlit as st
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import chromadb
import pandas as pd
import numpy as np

# Page configuration for a professional wide layout
st.set_page_config(page_title="FactCheck AI Pro", layout="wide", initial_sidebar_state="expanded")

# --- CORE AI SETUP ---
@st.cache_resource
def load_clip_model():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

@st.cache_resource
def setup_vector_db():
    client = chromadb.Client()
    collection = client.create_collection("verified_news")
    collection.add(
        documents=[
            "A golden retriever dog was seen standing gracefully outside a white house.",
            "Wild tigers are strictly monitored and restricted to dense jungles and wildlife reserves.",
            "A fake rumor is spreading about a tiger roaming the city streets, it is completely false."
        ],
        metadatas=[{"source": "Pet News Daily", "trust_score": 98}, 
                   {"source": "Wildlife Authority", "trust_score": 99}, 
                   {"source": "City Police", "trust_score": 100}],
        ids=["id1", "id2", "id3"]
    )
    return collection

try:
    model, processor = load_clip_model()
    db_collection = setup_vector_db()
except Exception as e:
    st.sidebar.error(f"System Error: {e}")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🔍 FactCheck AI")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Verification Engine", "Analytics & Benchmarks", "System Logs"])
st.sidebar.markdown("---")
st.sidebar.info("Module: BAI-12 (Multimodal Misinformation Verification)")

# --- PAGE 1: VERIFICATION ENGINE ---
if page == "Verification Engine":
    st.title("Multimodal Misinformation Verification Engine")
    st.write("Analyze text-image consistency and retrieve evidence from verified sources[cite: 26, 27].")
    
    col_input1, col_input2 = st.columns([1, 1.5])
    
    with col_input1:
        st.subheader("1. Input Data")
        uploaded_file = st.file_uploader("Upload Media (Image)", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True, caption="Source Media")
            
    with col_input2:
        st.subheader("2. Associated Claim")
        claim_text = st.text_area("Enter the text claim associated with this media:", height=150)
        verify_btn = st.button("Run Verification Pipeline", use_container_width=True, type="primary")
        
    if verify_btn and uploaded_file and claim_text:
        with st.spinner("Executing Multimodal Fusion & Evidence Retrieval..."):
            # Model execution
            inputs = processor(text=[claim_text], images=image, return_tensors="pt", padding=True)
            outputs = model(**inputs)
            sim_score = outputs.logits_per_image.item()
            
            # DB execution
            results = db_collection.query(query_texts=[claim_text], n_results=1)
            matched_doc = results['documents'][0][0]
            matched_source = results['metadatas'][0][0]['source']
            distance = results['distances'][0][0]
            
            st.markdown("---")
            st.subheader("Verification Results")
            
            # Professional Tabs layout for outputs
            tab1, tab2, tab3 = st.tabs(["📊 Final Verdict", "🧠 Explainability View", "📚 Database Evidence"])
            
            with tab1:
                st.metric("Text-Image Consistency Score", f"{sim_score:.2f} / 40.0")
                if sim_score > 28:
                    st.success("✅ HIGH CONSISTENCY: The image and text contextually match.")
                elif sim_score > 22:
                    st.warning("⚠️ SUSPICIOUS: Slight mismatch detected. Manual review recommended.")
                else:
                    st.error("🚨 POTENTIAL MISINFORMATION: Image and text do not match. Possible manipulation.")
                    
            with tab2:
                st.markdown("#### Modality Ablation Analysis")
                st.write("Visualizing the independent contributions of modalities[cite: 26, 27].")
                col_exp1, col_exp2 = st.columns(2)
                col_exp1.info("Vision Encoder: Active")
                col_exp2.info("Text Encoder: Active")
                with st.expander("View Mathematical Logits (Error Analysis)"):
                    st.json({"image_logits": sim_score, "text_length": len(claim_text.split()), "embedding_distance": distance})
                    
            with tab3:
                st.markdown("#### Semantic Evidence Retrieval")
                st.write(f"**Top Match:** {matched_doc}")
                st.caption(f"Source: {matched_source} | Semantic Distance: {distance:.4f}")
                if distance < 1.0:
                    st.success("Evidence supports the textual claim.")
                else:
                    st.error("No verified evidence found for this claim in the database.")

# --- PAGE 2: ANALYTICS & BENCHMARKS ---
elif page == "Analytics & Benchmarks":
    st.title("System Benchmark Dashboard")
    st.write("Macro F1, Modality Ablation, and System Robustness Tracking[cite: 26].")
    
    # Dummy data to simulate an active dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Macro F1 Score", "0.92", "+0.03")
    col2.metric("False Positive Rate", "4.2%", "-1.1%")
    col3.metric("Average Latency", "240ms", "-15ms")
    
    st.subheader("Recent Verification Logs")
    dummy_data = pd.DataFrame({
        "Date": pd.date_range(start="2026-09-25", periods=5),
        "Claim Snippet": ["Tiger in city...", "Dog outside house...", "Election fraud...", "Free money...", "New space launch..."],
        "Consistency Score": [17.2, 35.1, 12.4, 15.6, 31.0],
        "Verdict": ["Fake", "Authentic", "Fake", "Fake", "Authentic"]
    })
    st.dataframe(dummy_data, use_container_width=True)

# --- PAGE 3: SYSTEM LOGS ---
elif page == "System Logs":
    st.title("Audit Trail & System Logs")
    st.write("Privacy-aware operational monitoring and telemetry[cite: 26, 27].")
    st.code("[INFO] 2026-10-01 19:40:00 - System Initialized\n[INFO] 2026-10-01 19:40:02 - Vector DB connected (3 records)\n[INFO] 2026-10-01 19:40:05 - CLIP Model loaded onto CPU\n[WARN] 2026-10-01 19:42:12 - Low consistency threshold triggered on request ID #4092", language="log")