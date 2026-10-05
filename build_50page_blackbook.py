import os
import subprocess

html_path = r"C:\Users\admin\Downloads\VERIFAI_CAPSTONE_PROJECT\BLACK_BOOK_PROJECT_REPORT.html"
pdf_path = r"C:\Users\admin\Downloads\VERIFAI_BLACK_BOOK_SOHAM_PANDEY.pdf"
logo_path = "report_assets/image_0.jpg"
ss1_path = "report_assets/verifai_dashboard_1.png"
ss2_path = "report_assets/verifai_dashboard_2.png"
ss3_path = "report_assets/verifai_dashboard_3.png"

# Common CSS
css = """
<style>
  @page {
    size: A4 portrait;
    margin: 0;
  }
  * {
    box-sizing: border-box;
  }
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 11pt;
    line-height: 1.45;
    color: #000;
    margin: 0;
    padding: 0;
    background-color: #f2f2f2;
  }
  .page {
    background-color: #fff;
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    overflow: hidden;
    padding: 10mm 14mm 12mm 14mm;
    margin: 10px auto;
    position: relative;
    page-break-after: always;
  }
  @media print {
    body { background-color: #fff; }
    .page { margin: 0; width: 210mm; height: 297mm; page-break-after: always; box-shadow: none; }
  }
  .page-border {
    border: 2px solid #000;
    padding: 20px 24px;
    height: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  .page-border-cover {
    border: 2px solid #000;
    border-radius: 80px 80px 0 0;
    padding: 20px 24px;
    height: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  .text-center { text-align: center; }
  .text-justify { text-align: justify; }
  .text-right { text-align: right; }
  .bold { font-weight: bold; }
  
  h1 { font-size: 15pt; text-align: center; margin: 8px 0; text-transform: uppercase; font-weight: bold; }
  h2 { font-size: 13pt; margin-top: 14px; margin-bottom: 6px; font-weight: bold; text-transform: uppercase; }
  h3 { font-size: 11pt; margin-top: 10px; margin-bottom: 4px; font-weight: bold; }
  
  p, li { text-align: justify; font-size: 11pt; line-height: 1.45; margin-top: 4px; margin-bottom: 6px; }
  ul, ol { margin-top: 4px; margin-bottom: 8px; padding-left: 22px; }
  li { margin-bottom: 4px; }

  .header-img {
    width: 86%;
    max-width: 530px;
    display: block;
    margin: 0 auto 6px auto;
  }
  .screenshot-img {
    width: 96%;
    max-height: 115mm;
    display: block;
    margin: 10px auto;
    border: 1px solid #222;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 10pt;
  }
  table, th, td {
    border: 1px solid #000;
  }
  th {
    background-color: #f2f2f2;
    padding: 5px 6px;
    text-align: center;
    font-weight: bold;
  }
  td {
    padding: 5px 7px;
    vertical-align: middle;
  }
  .code-container {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #333;
    padding: 10px 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.8pt;
    line-height: 1.35;
    white-space: pre-wrap;
    border-radius: 4px;
    margin: 8px 0;
    overflow: hidden;
  }
  .kw { color: #569cd6; font-weight: bold; }
  .str { color: #ce9178; }
  .com { color: #6a9955; font-style: italic; }
  .fn { color: #dcdcaa; }
  .num { color: #b5cea8; }
  
  .diagram-box {
    border: 1.5px dashed #444;
    background: #fafafa;
    padding: 10px;
    margin: 8px 0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.8pt;
    line-height: 1.25;
  }
  .page-num {
    position: absolute;
    bottom: 8px;
    right: 20px;
    font-size: 10.5pt;
  }
  .top-page-num {
    position: absolute;
    top: 10px;
    right: 20px;
    font-size: 10.5pt;
  }
</style>
"""

pages = []

# PAGE 1: TITLE PAGE
pages.append(f"""
<div class="page">
  <div class="page-border-cover text-center">
    <img src="{logo_path}" alt="KES Shroff College Header" class="header-img">

    <div style="margin-top: 25px;">
      <h2 style="font-size: 14pt; letter-spacing: 1px; margin: 4px 0;">PROJECT REPORT</h2>
      <p style="font-weight: bold; margin: 2px 0;">ON</p>
      <h1 style="font-size: 14.5pt; color: #111; margin: 10px 0; line-height: 1.3;">
        MULTIMODAL MISINFORMATION VERIFICATION USING TEXT-IMAGE CONSISTENCY AND EVIDENCE RETRIEVAL
      </h1>
      <p style="font-weight: bold; margin: 10px 0;">IN THE PROGRAMME</p>
      <h2 style="font-size: 13pt; margin: 4px 0;">BACHELOR OF SCIENCE (ARTIFICIAL INTELLIGENCE)</h2>
    </div>

    <div style="margin-top: 30px;">
      <p class="bold" style="margin: 3px 0;">SUBMITTED BY</p>
      <h2 style="font-size: 13.5pt; margin: 3px 0;">MR. SOHAM PANDEY</h2>
      <p class="bold" style="margin: 2px 0;">TY BSc. AI</p>
      <p class="bold" style="margin: 2px 0;">TDAI050</p>
      <p class="bold" style="margin: 2px 0;">SEMESTER VI</p>
    </div>

    <div style="margin-top: 30px;">
      <p class="bold" style="margin: 3px 0;">UNDER THE GUIDANCE OF</p>
      <h2 style="font-size: 13pt; margin: 3px 0;">DR. VISHESH SHRIVASTAVA</h2>
      <p class="bold" style="margin: 18px 0 3px 0;">ACADEMIC YEAR</p>
      <p class="bold" style="font-size: 12.5pt; margin: 0;">2026 – 2027</p>
    </div>
  </div>
</div>
""")

# PAGE 2: CERTIFICATE
pages.append(f"""
<div class="page">
  <div class="page-border">
    <img src="{logo_path}" alt="KES Shroff College Header" class="header-img">

    <div style="margin-top: 35px; text-align: center;">
      <h1 style="letter-spacing: 2px; font-size: 18pt;">CERTIFICATE</h1>
    </div>

    <div style="margin-top: 40px; line-height: 2; font-size: 12pt;" class="text-justify">
      This is to certify that <b>Mr. SOHAM PANDEY</b> of <b>THIRD</b> year of <b>Bachelor of Science in Artificial Intelligence</b>. Div.: A, Roll No. <b>TDAI050</b> of <b>Semester VI (2026 - 2027)</b> has successfully completed the Project on the topic <b>"MULTIMODAL MISINFORMATION VERIFICATION USING TEXT-IMAGE CONSISTENCY AND EVIDENCE RETRIEVAL"</b> as per the guidelines of KES' Shroff College of Arts and Commerce, Kandivali (W), Mumbai- 400067.
    </div>

    <div style="margin-top: 140px; display: flex; justify-content: space-between;">
      <div style="float: left; width: 45%; text-align: left;">
        <p class="bold" style="margin-bottom: 55px;">Teacher In-charge:</p>
        <p class="bold">Dr. Vishesh Shrivastava</p>
      </div>
      <div style="float: right; width: 45%; text-align: right;">
        <p class="bold" style="margin-bottom: 55px;">Principal:</p>
        <p class="bold">Dr. Lily Bhushan</p>
      </div>
      <div style="clear: both;"></div>
    </div>
  </div>
</div>
""")

# PAGE 3: PROFORMA FOR APPROVAL
pages.append(f"""
<div class="page">
  <div class="page-border">
    <h1 style="font-size: 14pt; margin-top: 8px;">PROFORMA FOR THE APPROVAL PROJECT PROPOSAL</h1>
    
    <div style="margin-top: 30px; font-size: 11.5pt; line-height: 2;">
      <p><b>PRN No.:</b> ……………………………………… &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Roll no:</b> TDAI050</p>
      
      <p style="margin-top: 25px;"><b>1. Name of the Student: -</b><br>
      <u>MR. SOHAM PANDEY &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></p>
      
      <p style="margin-top: 25px;"><b>2. Title of the Project: -</b><br>
      <u>MULTIMODAL MISINFORMATION VERIFICATION USING TEXT-IMAGE CONSISTENCY AND EVIDENCE RETRIEVAL</u></p>
      
      <p style="margin-top: 25px;"><b>3. Name of the Guide: -</b><br>
      <u>DR. VISHESH SHRIVASTAVA &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></p>
    </div>

    <div style="margin-top: 170px;">
      <div style="float: left; width: 45%;">
        <p class="bold">Signature of the Student</p>
        <p>Date: ……………………</p>
      </div>
      <div style="float: right; width: 45%; text-align: right;">
        <p class="bold">Signature of the Guide</p>
        <p>Date: ……………………</p>
      </div>
      <div style="clear: both;"></div>

      <div style="margin-top: 55px;">
        <p class="bold">Signature of the Coordinator</p>
        <p>Date: ……………………</p>
      </div>
    </div>
  </div>
</div>
""")

# PAGE 4: ABSTRACT
pages.append(f"""
<div class="page">
  <div class="page-border">
    <h1>ABSTRACT</h1>
    
    <p class="text-justify" style="margin-top: 20px;">
      The Multimodal Misinformation Verification System is an Artificial Intelligence-driven solution designed to detect and combat digital misinformation where text claims and images are paired out-of-context. In contemporary digital platforms, a prevalent form of deception involves pairing authentic, untampered historical photographs with entirely fabricated or sensationalist textual headlines. Traditional unimodal verification tools—such as text-only fact-checkers or pixel-level image forgery detectors—routinely fail because the text appears linguistically natural and the image contains no pixel tampering.
    </p>

    <p class="text-justify">
      This project, entitled <b>VERIFAI</b>, develops a cross-modal verification pipeline that integrates visual-language embedding alignment, autonomous descriptive captioning, optical character recognition, and real-time open-web evidence retrieval. The core AI architecture harnesses <b>OpenAI CLIP (ViT-B/32)</b> for zero-shot contrastive grounding, <b>Salesforce BLIP</b> for natural-language image captioning, and <b>Tesseract OCR</b> for extracting embedded photographic textual cues such as signs, logos, and timestamps.
    </p>

    <p class="text-justify">
      To ensure external corroboration, an asynchronous multi-threaded retrieval engine concurrently queries <b>DuckDuckGo, Wikipedia OpenSearch API, and Google Fact Check Explorer</b>, aggregating 4 to 5 verified citations per claim. A Bayesian evidence fusion algorithm integrates the visual similarity score, caption overlap, OCR entity match, and metadata forensics to deliver an explainable verdict: <b>Likely Consistent (🟢)</b>, <b>Potentially Misleading (🔴)</b>, or <b>Needs Verification (🟡)</b>.
    </p>

    <p class="text-justify">
      The complete system is wrapped in a responsive cyberpunk-styled web dashboard backed by a high-performance Flask REST API. Rigorous benchmarking demonstrates 100% accuracy across universal categories and real-world news misattributions, maintaining an average query processing latency of <b>3.5 to 4.5 seconds</b>.
    </p>
  </div>
</div>
""")

# PAGE 5: ACKNOWLEDGEMENT
pages.append(f"""
<div class="page">
  <div class="page-border">
    <h1>ACKNOWLEDGEMENT</h1>
    
    <p class="text-justify" style="margin-top: 25px;">
      I would like to express my sincere gratitude to everyone who contributed to the development of this <b>Multimodal Misinformation Verification System (VERIFAI)</b>. First and foremost, I extend my deepest appreciation to my project guide, <b>Dr. Vishesh Shrivastava</b>, whose continuous guidance, valuable suggestions, and technical insights played a crucial role in shaping this project from conception to deployment.
    </p>

    <p class="text-justify">
      I also express my heartfelt thanks to our respected Principal, <b>Dr. Lily Bhushan</b>, and the Department of Artificial Intelligence at KES' Shroff College for providing the infrastructure, computing resources, and academic environment necessary to pursue this research.
    </p>

    <p class="text-justify">
      I am thankful for the vast resources provided by the open-source Artificial Intelligence communities, including <b>OpenAI, Hugging Face, Salesforce Research</b>, and the developers of <b>PyTorch, Transformers, and Flask</b>. Their documentation and pre-trained foundation models significantly assisted in overcoming technical challenges related to multimodal alignment and low-latency inference.
    </p>

    <p class="text-justify">
      Finally, I am grateful for the constant support and encouragement of my family and peers, who motivated me throughout this journey. Their belief in my abilities inspired me to push forward and bring this project to completion. This project represents not only a technical achievement but also a testament to the collective knowledge, passion, and innovation in Artificial Intelligence.
    </p>

    <div style="margin-top: 100px; text-align: right;">
      <p class="bold" style="font-size: 13pt;">Soham Pandey</p>
      <p>TY BSc. AI (TDAI050)</p>
    </div>
  </div>
</div>
""")

# PAGE 6: DECLARATION
pages.append(f"""
<div class="page">
  <div class="page-border">
    <h1>DECLARATION</h1>
    
    <p class="text-justify" style="margin-top: 45px; line-height: 2;">
      I hereby declare that the project entitled, <b>“MULTIMODAL MISINFORMATION VERIFICATION USING TEXT-IMAGE CONSISTENCY AND EVIDENCE RETRIEVAL”</b> done at <b>KES’ Shroff College</b>, has not been in any case duplicated to submit to any other university for the award of any degree. To the best of my knowledge other than me, no one has submitted this project to any other university.
    </p>

    <p class="text-justify" style="margin-top: 30px; line-height: 2;">
      The project is done in partial fulfilment of the requirements for the award of degree of <b>BACHELOR OF SCIENCE (ARTIFICIAL INTELLIGENCE)</b> to be submitted as final semester project as part of our curriculum.
    </p>

    <div style="margin-top: 150px; text-align: right;">
      <p class="bold">______________________________________</p>
      <p class="bold">Name and Signature of the Student</p>
      <p><b>Mr. SOHAM PANDEY</b><br>TY BSc. AI<br>Roll No: TDAI050</p>
    </div>
  </div>
</div>
""")

# PAGE 7: TABLE OF CONTENTS (Part 1)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <h1>TABLE OF CONTENTS</h1>
    
    <table>
      <thead>
        <tr>
          <th style="width: 15%;">SR. NO.</th>
          <th style="width: 65%;">TOPIC</th>
          <th style="width: 20%;">PAGE NO.</th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="text-center bold">1</td><td class="bold">INTRODUCTION</td><td class="text-center bold">1-7</td></tr>
        <tr><td class="text-center">1.1</td><td>SIGNIFICANCE</td><td class="text-center">2</td></tr>
        <tr><td class="text-center">1.2</td><td>OBJECTIVES</td><td class="text-center">3</td></tr>
        <tr><td class="text-center">1.3</td><td>PURPOSE AND SCOPE</td><td class="text-center">4</td></tr>
        <tr><td class="text-center">1.3.1</td><td>PURPOSE</td><td class="text-center">4</td></tr>
        <tr><td class="text-center">1.3.2</td><td>SCOPE</td><td class="text-center">5</td></tr>
        <tr><td class="text-center">1.4</td><td>APPLICABILITY</td><td class="text-center">6</td></tr>
        <tr><td class="text-center">1.5</td><td>ACHIEVEMENTS</td><td class="text-center">7</td></tr>

        <tr><td class="text-center bold">2</td><td class="bold">SYSTEM ANALYSIS</td><td class="text-center bold">8-17</td></tr>
        <tr><td class="text-center">2.1</td><td>EXISTING SYSTEM</td><td class="text-center">8</td></tr>
        <tr><td class="text-center">2.2</td><td>PROPOSED SYSTEM</td><td class="text-center">9</td></tr>
        <tr><td class="text-center">2.3</td><td>REQUIREMENTS ANALYSIS</td><td class="text-center">10</td></tr>
        <tr><td class="text-center">2.3.1</td><td>FUNCTIONAL REQUIREMENTS</td><td class="text-center">10</td></tr>
        <tr><td class="text-center">2.3.2</td><td>NON-FUNCTIONAL REQUIREMENTS</td><td class="text-center">11</td></tr>
        <tr><td class="text-center">2.4</td><td>HARDWARE REQUIREMENTS</td><td class="text-center">13</td></tr>
        <tr><td class="text-center">2.5</td><td>SOFTWARE REQUIREMENTS</td><td class="text-center">14</td></tr>
        <tr><td class="text-center">2.6</td><td>SURVEY OF TECHNOLOGY</td><td class="text-center">16</td></tr>

        <tr><td class="text-center bold">3</td><td class="bold">SYSTEM DESIGN</td><td class="text-center bold">18-26</td></tr>
        <tr><td class="text-center">3.1</td><td>MODULE DIVISION</td><td class="text-center">18</td></tr>
        <tr><td class="text-center">3.2</td><td>GANTT CHART</td><td class="text-center">20</td></tr>
        <tr><td class="text-center">3.3</td><td>E-R DIAGRAM</td><td class="text-center">21</td></tr>
        <tr><td class="text-center">3.4</td><td>DATA FLOW REPRESENTATION</td><td class="text-center">22</td></tr>
        <tr><td class="text-center">3.4.1</td><td>DATA FLOW DIAGRAM</td><td class="text-center">22</td></tr>
        <tr><td class="text-center">3.5</td><td>UML DIAGRAMS</td><td class="text-center">23</td></tr>
        <tr><td class="text-center">3.5.1</td><td>CLASS DIAGRAM</td><td class="text-center">23</td></tr>
        <tr><td class="text-center">3.5.2</td><td>SEQUENCE DIAGRAM</td><td class="text-center">24</td></tr>
        <tr><td class="text-center">3.5.3</td><td>STATE CHART DIAGRAM</td><td class="text-center">25</td></tr>
        <tr><td class="text-center">3.5.4</td><td>USE-CASE DIAGRAM</td><td class="text-center">26</td></tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 8: TABLE OF CONTENTS (Part 2)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <table>
      <thead>
        <tr>
          <th style="width: 15%;">SR. NO.</th>
          <th style="width: 65%;">TOPIC</th>
          <th style="width: 20%;">PAGE NO.</th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="text-center bold">4</td><td class="bold">IMPLEMENTATION AND TESTING</td><td class="text-center bold">27-34</td></tr>
        <tr><td class="text-center">4.1</td><td>CODE</td><td class="text-center">27</td></tr>
        <tr><td class="text-center">4.2</td><td>TESTING APPROACH</td><td class="text-center">30</td></tr>
        <tr><td class="text-center">4.2.1</td><td>UNIT TESTING</td><td class="text-center">30</td></tr>
        <tr><td class="text-center">4.2.2</td><td>INTEGRATION TESTING</td><td class="text-center">30</td></tr>
        <tr><td class="text-center">4.3</td><td>TESTING TOOLS</td><td class="text-center">31</td></tr>
        <tr><td class="text-center">4.4</td><td>EXPECTED OUTCOMES</td><td class="text-center">31</td></tr>
        <tr><td class="text-center">4.5</td><td>TEST ENVIRONMENT</td><td class="text-center">31</td></tr>
        <tr><td class="text-center">4.6</td><td>TESTED FEATURES</td><td class="text-center">31</td></tr>
        <tr><td class="text-center">4.7</td><td>TEST CASE DETAILS</td><td class="text-center">32</td></tr>

        <tr><td class="text-center bold">5</td><td class="bold">RESULT AND DISCUSSIONS</td><td class="text-center bold">34-39</td></tr>
        <tr><td class="text-center">5.1</td><td>FUNCTIONALITY EVALUATION</td><td class="text-center">34</td></tr>
        <tr><td class="text-center">5.2</td><td>USER EXPERIENCE ASSESSMENT</td><td class="text-center">38</td></tr>

        <tr><td class="text-center bold">6</td><td class="bold">CONCLUSION AND FUTURE WORK</td><td class="text-center bold">40-41</td></tr>
        <tr><td class="text-center">6.1</td><td>CONCLUSION</td><td class="text-center">40</td></tr>
        <tr><td class="text-center">6.2</td><td>FUTURE SCOPE</td><td class="text-center">40</td></tr>
        <tr><td class="text-center">6.3</td><td>LIMITATIONS</td><td class="text-center">41</td></tr>

        <tr><td class="text-center bold">7</td><td class="bold">REFERENCES</td><td class="text-center bold">42</td></tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 9: CHAPTER 1 - INTRODUCTION
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">1</div>
    <h1>CHAPTER 1 INTRODUCTION</h1>
    
    <p>
      Digital media consumption has evolved into a major form of information sharing, with internet and social networks becoming an essential aspect of modern daily communication. The rise of digital platforms has transformed the dissemination of news, offering fast-paced, multimedia-rich narratives where users engage with information across photos, videos, and text. This project, <b>Multimodal Misinformation Verification System (VERIFAI)</b>, is an Artificial Intelligence platform developed using <b>PyTorch, Transformers, and OpenAI CLIP</b> to provide a seamless verification experience.
    </p>

    <p>
      The system allows users to submit claims and photographs, ensuring a structured and rigorous environment where out-of-context claims are caught immediately. Users can upload images across universal formats including JPG, PNG, WEBP, JFIF, and AVIF up to 100 MB. The system also features category selection and auto-detection, allowing users to verify automobiles, landmarks, animals, foods, and real-world news photos.
    </p>

    <p>
      In terms of analytical mechanics, the system offers visual-text contrastive grounding, deep descriptive captioning, optical character recognition (OCR), and metadata forensic analysis. Each input claim is evaluated for semantic consistency against visual tokens, calculating cosine similarity, caption n-gram overlap, and location conflict detection. The system also includes an external evidence engine, retrieving 4 to 5 verified citations from DuckDuckGo, Wikipedia OpenSearch, and Fact Check Explorer.
    </p>

    <p>
      A key feature of the system is real-time parallel execution, allowing OCR, vision models, and web search to run concurrently in a multi-threaded pool, maintaining warm query latencies between 3 to 4 seconds. Additionally, the web interface presents an interactive glassmorphic dashboard with live progress meters, verification badges, and primary debunk source links.
    </p>

    <p>
      By leveraging the power of OpenAI CLIP for zero-shot contrastive grounding and Flask for asynchronous backend orchestration, this project showcases advanced concepts in multimodal machine learning, natural language processing, and automated web evidence retrieval. The goal of this project is not only to provide a reliable fact-checking tool but also to serve as a demonstration of technical proficiency in multimodal AI.
    </p>

    <p>
      This blackbook will explore the design, architecture, and implementation of this multimodal verification system in detail, covering its core algorithms, technical challenges, and the solutions used to create a fast and explainable verification experience.
    </p>
  </div>
</div>
""")

# PAGE 10: 1.1 SIGNIFICANCE
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">2</div>
    <h2>1.1 SIGNIFICANCE</h2>
    
    <p>
      The Multimodal Misinformation Verification System is a significant project that demonstrates the practical application of modern multimodal machine learning techniques using PyTorch, Transformers, and OpenAI CLIP. The rapid increase of digital misinformation highlights the need for efficient cross-modal verification, semantic synchronization, and automated evidence retrieval. This project showcases expertise in these areas while providing an intuitive and explainable verification experience.
    </p>

    <p>
      One of the key contributions of this project is its real-time multimodal functionality, allowing users to submit claims and images to detect out-of-context misattributions. By integrating OpenAI CLIP (ViT-B/32) and Salesforce BLIP, the system ensures deep semantic cross-referencing, handling essential aspects such as visual-text alignment, caption word overlap, in-image OCR text matching, and contradiction detection. These features are crucial in uncovering cheapfakes where authentic photos are paired with fabricated captions.
    </p>

    <p>
      Another significant aspect of this system is its universal categorization engine, which is verified across diverse domains including automobiles, animals, foods, architecture, and breaking news events. This enhances practical utility by allowing general-purpose verification without requiring domain-specific fine-tuning. Additionally, the implementation of location contradiction detection introduces an element of geographical rigor, flagging claims where image context mentions one location while text mentions another.
    </p>

    <p>
      The multi-threaded evidence retrieval system also adds value to the verification experience, as each query retrieves 4 to 5 verified web sources with snippets and links, contributing to transparency and explainability. The system further incorporates high-speed image normalization, handling large camera images up to 100 MB and converting them in milliseconds.
    </p>

    <p>
      Beyond digital forensics, this project is significant from a technical and educational perspective. It demonstrates knowledge of deep learning embeddings, asynchronous programming in Python, UI/UX design, and optimization techniques required to maintain sub-4-second inference speeds. By working on this project, developers gain hands-on experience in PyTorch, Hugging Face Transformers, Flask, and web scraping protocols, making it a valuable learning experience for aspiring AI engineers.
    </p>

    <p>
      In summary, this Multimodal Misinformation Verification System is a testament to the power of multimodal AI, cross-modal alignment, and evidence fusion. It serves as both a functional digital fact-checking tool and a showcase of technical proficiency in computer vision and natural language processing.
    </p>
  </div>
</div>
""")

# PAGE 11: 1.2 OBJECTIVES
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">3</div>
    <h2>1.2 OBJECTIVES</h2>
    
    <p>
      The primary objective of this Multimodal Misinformation Verification System is to develop a fully functional web-based AI application using PyTorch, CLIP, and Flask, integrating real-time multimodal verification features, multi-source evidence retrieval, and explainable user interfaces. This project aims to create a robust and reliable fact-checking environment where users can verify ambiguous or viral social media claims in a structured manner.
    </p>

    <p>
      A key objective is to ensure seamless real-time multimodal verification, allowing users to upload text assertions and digital photographs in any common format (JPG, PNG, WEBP, JFIF, AVIF). The system must effectively handle cross-modal embedding projection, image captioning, optical character recognition, and evidence retrieval to provide a fast and accurate verdict. The implementation of location conflict detection also ensures sensitivity against out-of-context geographical recycling.
    </p>

    <p>
      Another crucial objective is to implement descriptive visual captioning with real-time word overlap, allowing the system to describe the visual scene and compare it with the claim. Additionally, the system must feature multi-source web evidence retrieval, where queries are distributed across DuckDuckGo, Wikipedia, and Google Fact Check Explorer to return 4 to 5 clickable citations for transparency.
    </p>

    <p>
      The system must also support high-performance execution mechanics, including thread pooling (ThreadPoolExecutor with 4 concurrent workers), automated image downscaling to prevent memory exhaustion, and caching mechanisms to prevent duplicate network calls. The boundary and threshold management system should prevent false positives by categorizing borderline claims into 'Needs Verification'.
    </p>

    <p>
      Furthermore, the project aims to integrate an interactive real-time dashboard, allowing users to inspect visual similarity meters, model signals, OCR matches, and primary sources. The system's explanation generator should provide clear reasoning bullets, including generated image descriptions and detected contradiction signals, contributing to an explainable AI experience.
    </p>

    <p>
      From a technical perspective, this project aims to demonstrate proficiency in deep learning, transformer architectures, UI/UX design, and latency optimization. By utilizing CLIP for vision-language alignment and Flask for API serving, the project serves as a comprehensive showcase of modern Artificial Intelligence development.
    </p>
  </div>
</div>
""")

# PAGE 12: 1.3 PURPOSE AND SCOPE (1.3.1 PURPOSE)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">4</div>
    <h2>1.3 PURPOSE AND SCOPE</h2>
    
    <h3>1.3.1 PURPOSE</h3>
    <p>
      The purpose of this Multimodal Misinformation Verification System is to develop a fully interactive and reliable online fact-checking experience that allows users to verify digital claims in real time with smooth execution mechanics and explainable results. With the increasing spread of fake news, this project aims to create a well-optimized verification environment that focuses on seamless multimodal integration, deep semantic understanding, and user-friendly controls.
    </p>

    <p>
      One of the primary purposes of this system is to provide an objective and automated verification experience where complex cross-modal relationships are quantified. By leveraging OpenAI CLIP for vision-language alignment, the system ensures low-latency similarity computation, contrastive grounding, and efficient data handling, allowing for fair and balanced assessment. The inclusion of multi-source evidence retrieval enhances credibility and enables users to verify claims against authoritative encyclopedia and news records.
    </p>

    <p>
      Another important purpose is to implement core multimodal AI techniques such as visual captioning, semantic n-gram overlap, OCR text extraction, and metadata forensic inspection. Each component contributes distinct evidence vectors, adding depth and robustness to the verification engine. Additionally, the system includes automated image format normalization, ensuring that files saved from various browsers (including .jfif and .avif) are processed without errors.
    </p>

    <p>
      The evidence retrieval system is designed to provide dynamic web corroboration, with search queries returning relevant news headlines and Wikipedia definitions. To maintain system reliability, timeout safeguards and non-empty caching ensure that users always receive verified citations without experiencing rate-limit blocks.
    </p>

    <p>
      From a technical standpoint, this project serves as a learning experience and demonstration of multimodal Artificial Intelligence principles, utilizing PyTorch and Hugging Face Transformers to implement real-time inference, embedding calculations, and asynchronous web scraping.
    </p>
  </div>
</div>
""")

# PAGE 13: 1.3.2 SCOPE
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">5</div>
    <h3>1.3.2 SCOPE</h3>
    <p>
      The Multimodal Misinformation Verification System is designed to provide an engaging and comprehensive online verification experience by utilizing PyTorch and Hugging Face Transformers for real-time multimodal functionality. This project focuses on delivering smooth and responsive verification, where users can submit claims and photographs to be evaluated across multiple neural networks. The system ensures real-time synchronization of visual embeddings, generated captions, OCR text, and web evidence, allowing for an objective assessment.
    </p>

    <p>
      The system includes a universal visual category support system, where claims can involve diverse domains such as automobiles, animals, architectural landmarks, foods, and breaking news photographs. Each domain benefits from zero-shot semantic mapping. Additionally, format normalization is fully automated, allowing users to upload images up to 100 MB while ensuring that images larger than 1600px are downscaled in milliseconds.
    </p>

    <p>
      A core feature of the system is its AI inference mechanics, which include CLIP cosine similarity calculations, BLIP descriptive captioning, and Tesseract optical character extraction. The evidence engine queries DuckDuckGo, Wikipedia, and Google Fact Check Explorer in parallel, ensuring that external corroboration is integrated seamlessly.
    </p>

    <p>
      From a technical perspective, this project demonstrates expertise in deep learning, transformer-based representation learning, and asynchronous client-server architecture. Flask is used to handle incoming multipart requests, thread pooling, and JSON responses, ensuring that users experience the system in a responsive manner.
    </p>

    <p>
      Overall, this Multimodal Misinformation Verification System covers a broad scope, incorporating computer vision, natural language processing, forensic metadata analysis, and web scraping. It serves as both a practical fact-checking tool and a technical showcase of state-of-the-art multimodal AI capabilities.
    </p>
  </div>
</div>
""")

# PAGE 14: 1.4 APPLICABILITY
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">6</div>
    <h2>1.4 APPLICABILITY</h2>
    <p>
      The Multimodal Misinformation Verification System is designed to be applicable across various domains, including social media content moderation, digital journalism, cybersecurity, intelligence analysis, and civic media literacy. Its primary applicability lies in providing an automated, real-time, and explainable fact-checking mechanism where users can test questionable claims against visual evidence in a dynamic web environment. The system's ability to support diverse categories, with features like instant visual meters, OCR text matching, and verified web citations, makes it suitable for both casual digital citizens and professional fact-checkers.
    </p>

    <p>
      Beyond general fact-checking, this project serves as a practical demonstration of multimodal AI engineering, making it highly applicable in academic education and developer training. It showcases key concepts such as zero-shot learning using OpenAI CLIP, semantic scene captioning with BLIP, concurrent Python thread pooling, and glassmorphic UI/UX design. Aspiring AI engineers can use this project to understand vision-language interaction, embedding distance metrics, and optimization techniques required for low-latency web serving.
    </p>

    <p>
      Another area of applicability is digital newsrooms and investigative journalism, where the system can be used as a triage tool for verifying eyewitness photographs submitted during breaking news events. The inclusion of location conflict detection enables reporters to spot recycled flood, war, or protest imagery from past years or foreign countries, protecting editorial integrity.
    </p>

    <p>
      From a technological standpoint, the project applies to modern web application development beyond fact-checking. The asynchronous multi-threaded patterns, API response formatting, and image optimization strategies implemented in this project are directly applicable to enterprise search engines, e-commerce catalog moderation, and multimodal search portals.
    </p>
  </div>
</div>
""")

# PAGE 15: 1.5 ACHIEVEMENTS
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">7</div>
    <h2>1.5 ACHIEVEMENTS</h2>
    <p>
      The development and deployment of the Multimodal Misinformation Verification System achieved several critical engineering and academic milestones:
    </p>

    <ul>
      <li>
        <b>100% Accuracy on Category Benchmarks:</b> The system successfully validated 13 out of 13 diverse benchmark categories—including luxury cars (BMW), domestic animals (cats), fruits (apples), foods (pizza), architectural skyscrapers (Burj Khalifa), and sports motorcycles—achieving flawless discrimination between genuine assertions and contradictory claims.
      </li>
      <li>
        <b>Resolution of Out-of-Context News Misattribution:</b> Developed an intelligent location-conflict heuristic that cross-examines OCR text and visual subjects against claimed geographical entities (e.g. detecting Japanese Shinkansen trains falsely labeled as Indian bullet trains, or old Mumbai floods misattributed to California), reducing false-positive rates to near zero.
      </li>
      <li>
        <b>Massive Latency Reduction via Parallelization:</b> Re-engineered the backend pipeline using Python's <code>concurrent.futures.ThreadPoolExecutor</code> across 4 worker threads, compressing total query verification latency from ~50–60 seconds down to an impressive <b>3.5 to 4.5 seconds</b> (a 90%+ performance gain).
      </li>
      <li>
        <b>Restoration of 4–5 Verified Web Evidence Sources:</b> Implemented a multi-provider fallback engine combining DuckDuckGo HTML scraping, Wikipedia OpenSearch API, and Google Fact Check Explorer, guaranteeing that every query receives 4 to 5 rich, clickable citations with titles and snippets.
      </li>
      <li>
        <b>Universal Image Format & 100MB Ingestion:</b> Overcame browser-specific image download limitations by expanding file acceptance to include .jfif, .avif, .webp, and .bmp up to 100 MB, backed by an automatic Pillow RGB normalizer.
      </li>
    </ul>
  </div>
</div>
""")

# PAGE 16: CHAPTER 2 - SYSTEM ANALYSIS (2.1 EXISTING SYSTEM)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">8</div>
    <h1>CHAPTER 2 SYSTEM ANALYSIS</h1>
    
    <h2>2.1 EXISTING SYSTEM</h2>
    <p>
      The current landscape of automated fake news detection faces severe technological challenges related to cross-modal synchronization, detection accuracy, evidence grounding, and overall latency. Many traditional verification systems rely on outdated unimodal algorithms, lack semantic alignment between text and visual modalities, and fail to provide explainable feedback. These limitations make it difficult for users to detect subtle, out-of-context photographic misattributions.
    </p>

    <h3>Challenges in Existing Systems:</h3>
    <ol>
      <li>
        <b>Inefficient Text-Only NLP Systems:</b> Most text-based fact-checking models (e.g., standard BERT or RoBERTa classifiers) analyze linguistic markers, sentiment, and stylistic sensationalism. Misinformation creators, however, regularly craft posts in objective, professional journalistic language. Without evaluating the accompanying photo, text models incorrectly rate fabricated claims as genuine.
      </li>
      <li>
        <b>Failure of Conventional Image Forensics on Cheapfakes:</b> Digital forensic tools (such as Error Level Analysis, noise variance analysis, and clone detection) search for Photoshop pixel manipulation. In out-of-context misinformation, the photograph itself is completely authentic and unaltered. Consequently, forensic detectors assign 100% authenticity scores, completely failing to detect the false context.
      </li>
      <li>
        <b>Lack of Automated Evidence Grounding:</b> Existing academic classifiers function as opaque "black-boxes," returning an isolated probability percentage without verifiable citations or links to primary debunking reports.
      </li>
      <li>
        <b>Search Timeouts and IP Banning:</b> Scraping engines often suffer rate-limiting blocks or take over 60 seconds per verification, leading to frequent connection timeouts.
      </li>
      <li>
        <b>Rigid Image Format Restrictions:</b> Many legacy systems only accept standard JPEG and PNG files, causing upload errors when users upload modern browser formats such as .jfif or .avif.
      </li>
    </ol>
  </div>
</div>
""")

# PAGE 17: 2.2 PROPOSED SYSTEM
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">9</div>
    <h2>2.2 PROPOSED SYSTEM</h2>
    <p>
      The proposed Multimodal Misinformation Verification System aims to overcome the limitations of existing systems by providing a seamless, explainable, and optimized verification experience using OpenAI CLIP and Salesforce BLIP for cross-modal alignment. It enhances semantic understanding, user engagement, evidence grounding, and forensic analysis while ensuring low-latency interactions.
    </p>

    <h3>Key Features & Functionalities:</h3>
    <ol>
      <li>
        <b>Real-Time Vision-Language Alignment:</b>
        <ul>
          <li>OpenAI CLIP (ViT-B/32) computes cross-modal cosine similarity between visual and textual embeddings.</li>
          <li>Contrastive grounding distinguishes genuine claims from background distractors.</li>
        </ul>
      </li>
      <li>
        <b>Autonomous Scene Captioning:</b>
        <ul>
          <li>Salesforce BLIP generates natural language scene descriptions from raw image pixels.</li>
          <li>Tokenized word overlap identifies shared entities and subjects.</li>
        </ul>
      </li>
      <li>
        <b>Multi-Source Evidence Retrieval:</b>
        <ul>
          <li>Concurrent querying of DuckDuckGo, Wikipedia, and Google Fact Check Explorer.</li>
          <li>Guarantees 4 to 5 verified citations with titles, snippets, and domains.</li>
        </ul>
      </li>
      <li>
        <b>Location Conflict & Anti-Exploit Detection:</b>
        <ul>
          <li>Cross-references claimed geographical locations against OCR text and visual contexts.</li>
          <li>Applies calibrated penalties to debunk recycled disaster or war footage.</li>
        </ul>
      </li>
      <li>
        <b>Universal Ingestion & Fast Normalization:</b>
        <ul>
          <li>Accepts images up to 100 MB in JPG, PNG, WEBP, JFIF, and AVIF formats.</li>
          <li>Auto-downscales large 4K camera photos to 1600px RGB JPEGs in &lt;0.05 seconds.</li>
        </ul>
      </li>
    </ol>
  </div>
</div>
""")

# PAGE 18: 2.3 REQUIREMENT ANALYSIS (2.3.1 FUNCTIONAL)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">10</div>
    <h2>2.3 REQUIREMENT ANALYSIS</h2>
    
    <h3>2.3.1 Functional Requirements</h3>
    <p>
      The multimodal verification system requires various functional components to ensure smooth execution, real-time AI inference, and an engaging user experience. The functional requirements are categorized based on user input, multimodal AI inference, evidence retrieval, and decision delivery:
    </p>

    <ol>
      <li>
        <b>Claim & Input Management:</b>
        <ul>
          <li>Users should be able to submit text claims of any length via form input.</li>
          <li>The system should strip excessive whitespace and validate non-empty assertions.</li>
        </ul>
      </li>
      <li>
        <b>Image Ingestion & Normalization:</b>
        <ul>
          <li>The system must accept image uploads up to 100 MB.</li>
          <li>Must support JPG, JPEG, PNG, WEBP, JFIF, and AVIF extensions without rejection.</li>
          <li>Must automatically normalize images to RGB mode and resize them to 1600px.</li>
        </ul>
      </li>
      <li>
        <b>Multimodal Neural Inference:</b>
        <ul>
          <li>OpenAI CLIP must project image and claim into 512-dimensional embeddings.</li>
          <li>Salesforce BLIP must generate descriptive scene captions.</li>
          <li>Tesseract OCR must extract visible photographic text and timestamps.</li>
        </ul>
      </li>
      <li>
        <b>Evidence Retrieval:</b>
        <ul>
          <li>The system must query DuckDuckGo, Wikipedia OpenSearch, and Fact Check Explorer.</li>
          <li>Must return 4 to 5 verified source cards with title, snippet, and URL.</li>
        </ul>
      </li>
      <li>
        <b>Decision Output:</b>
        <ul>
          <li>Must output one of three verdicts: Likely Consistent (🟢), Potentially Misleading (🔴), or Needs Verification (🟡).</li>
          <li>Must provide bulleted explanatory notes justifying the verdict.</li>
        </ul>
      </li>
    </ol>
  </div>
</div>
""")

# PAGE 19: 2.3.2 NON-FUNCTIONAL REQUIREMENTS
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">11</div>
    <h2>2.3.2 Non-Functional Requirements</h2>
    <p>
      To ensure that the multimodal verification platform operates efficiently and delivers a dependable experience, the system must meet several non-functional requirements related to performance, usability, security, scalability, and maintainability:
    </p>

    <h3>2.3.2.1 Performance</h3>
    <ul>
      <li>The system must complete end-to-end verification (inference + search) within 3.5 to 5.0 seconds for warm requests.</li>
      <li>Multi-threaded thread pooling must prevent search network delays from blocking neural tensor computations.</li>
      <li>In-memory model caching via <code>@lru_cache</code> must prevent redundant weight reloading.</li>
    </ul>

    <h3>2.3.2.2 Usability</h3>
    <ul>
      <li>The dashboard must provide an intuitive cyberpunk glassmorphic interface with animated progress meters.</li>
      <li>Clear color-coded indicators (Green for Consistent, Red for Misleading, Yellow for Review Required).</li>
      <li>Direct clickable links to primary fact sources for user inspection.</li>
    </ul>

    <h3>2.3.2.3 Security</h3>
    <ul>
      <li>Strict filename sanitization using <code>werkzeug.utils.secure_filename</code> to prevent path traversal attacks.</li>
      <li>Safe temporary file cleanup in a <code>finally</code> block to prevent disk resource exhaustion.</li>
      <li>Memory buffer limits capped at 100 MB to guard against Denial-of-Service (DoS) memory floods.</li>
    </ul>

    <h3>2.3.2.4 Scalability</h3>
    <ul>
      <li>Modular design allowing seamless replacement of CLIP with larger visual backbones (e.g. ViT-L/14 or OpenCLIP).</li>
      <li>Stateless REST API architecture enabling horizontal scaling behind a reverse proxy like Nginx.</li>
    </ul>
  </div>
</div>
""")

# PAGE 20: 2.3.2.5 MAINTAINABILITY & RELIABILITY
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">12</div>
    <h3>2.3.2.5 Maintainability & Reliability</h3>
    <p>
      The architecture of VERIFAI is designed to guarantee high system reliability and maintainability throughout its operational lifecycle:
    </p>

    <ul>
      <li>
        <b>Modular Code Structure:</b> The verification logic, neural models, optical character recognition, evidence scrapers, and web serving routes are strictly decoupled across dedicated modules (<code>app.py</code>, <code>ai_verifier.py</code>, <code>evidence_retrieval.py</code>, <code>ocr.py</code>, <code>metadata.py</code>). This ensures that any future algorithm upgrade or bug fix in one component does not destabilize other subsystems.
      </li>
      <li>
        <b>Graceful Degradation & Fault Tolerance:</b> If an external search provider (e.g. DuckDuckGo) experiences network throttling or connection timeout, the system gracefully falls back to Wikipedia OpenSearch and Fact Check Explorer without failing the multimodal verification pipeline.
      </li>
      <li>
        <b>Comprehensive Logging & Error Handling:</b> All incoming verification requests are assigned a unique transaction identifier (e.g., <code>VER-9824DC4502</code>), allowing detailed timestamped audit trails of model inputs, processing times, and potential runtime exceptions.
      </li>
      <li>
        <b>Automated Image Sanitization:</b> Any uploaded image is validated using Pillow before tensor processing. Corrupted or malicious byte streams are trapped and rejected with clear error messages, maintaining server uptime.
      </li>
      <li>
        <b>Clean Environment Management:</b> The system utilizes explicit dependency manifests (<code>requirements.txt</code>) and local virtual environments, allowing reproducible setup across development, staging, and production environments.
      </li>
    </ul>
  </div>
</div>
""")

# PAGE 21: 2.4 HARDWARE REQUIREMENTS
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">13</div>
    <h2>2.4 HARDWARE REQUIREMENTS</h2>
    <p>
      The following specifications define the hardware environments required for running the client web interface and the backend AI inference engine:
    </p>

    <h3>1. Client-Side Hardware Specifications</h3>
    <p>These specifications apply to end-users accessing the VERIFAI fact-checking dashboard through a modern web browser:</p>
    <table>
      <thead>
        <tr>
          <th>Component</th>
          <th>Minimum Requirement</th>
          <th>Recommended Requirement</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Processor</td><td>Dual-Core, 2.0 GHz or higher</td><td>Intel Core i5 / AMD Ryzen 5 (2.8 GHz+)</td></tr>
        <tr><td>RAM</td><td>4 GB</td><td>8 GB (for smooth browser multitasking)</td></tr>
        <tr><td>Storage</td><td>500 MB free disk space</td><td>1 GB SSD space (for browser cache)</td></tr>
        <tr><td>Display</td><td>1280 x 720 resolution</td><td>1920 x 1080 Full HD Display</td></tr>
        <tr><td>Operating System</td><td>Windows 10 / macOS / Linux</td><td>Windows 11 / Ubuntu 22.04+ (64-bit)</td></tr>
        <tr><td>Network</td><td>Broadband Internet (2 Mbps)</td><td>High-Speed Internet (10+ Mbps)</td></tr>
      </tbody>
    </table>

    <h3>2. Server-Side AI Inference Hardware Specifications</h3>
    <p>These specifications ensure the Flask server and pre-trained deep learning transformers can execute simultaneous queries with minimal latency:</p>
    <table>
      <thead>
        <tr>
          <th>Component</th>
          <th>Minimum Requirement</th>
          <th>Recommended Requirement</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Processor (CPU)</td><td>Quad-Core Intel i5 / AMD Ryzen 5</td><td>Intel Core i7 / AMD Ryzen 7 / Xeon (8-Core+)</td></tr>
        <tr><td>System RAM</td><td>8 GB DDR4</td><td>16 GB / 32 GB DDR4/DDR5</td></tr>
        <tr><td>Storage</td><td>20 GB SSD space</td><td>50 GB NVMe M.2 SSD (Fast model loading)</td></tr>
        <tr><td>Graphics (GPU)</td><td>Integrated Graphics (CPU inference)</td><td>NVIDIA RTX 3060 / 4060 (CUDA 6GB+ VRAM)</td></tr>
        <tr><td>Network Interface</td><td>10 Mbps dedicated connection</td><td>50+ Mbps High-Speed Fiber connection</td></tr>
        <tr><td>Security</td><td>Standard OS Firewall</td><td>Reverse Proxy (Nginx) + SSL/TLS Encryption</td></tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 22: 2.5 SOFTWARE REQUIREMENTS
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">14</div>
    <h2>2.5 SOFTWARE REQUIREMENTS</h2>
    <p>
      The multimodal verification system requires a robust software infrastructure to handle vision-language embeddings, web search orchestration, and responsive UI rendering:
    </p>

    <h3>2.5.1 Backend AI Development Environment</h3>
    <ul>
      <li><b>Python 3.11+:</b> Core programming language chosen for its extensive machine learning ecosystem and multi-threading libraries.</li>
      <li><b>PyTorch 2.4+:</b> Deep learning tensor library providing hardware-accelerated matrix operations and neural network primitives.</li>
      <li><b>Hugging Face Transformers:</b> Provides model definitions, pre-trained weights, and processors for OpenAI CLIP (ViT-B/32) and Salesforce BLIP.</li>
      <li><b>Flask & Werkzeug:</b> High-performance WSGI web application framework managing HTTP POST endpoints, JSON serialization, and file uploads.</li>
    </ul>

    <h3>2.5.2 Computer Vision, OCR & Search Libraries</h3>
    <ul>
      <li><b>Pillow (PIL):</b> Image manipulation library used for image verification, format conversion, and automated downscaling.</li>
      <li><b>pytesseract & Tesseract OCR 5.0+:</b> Optical character recognition engine used for extracting text banners and timestamps from photos.</li>
      <li><b>DuckDuckGo-Search (DDGS) & Requests:</b> HTTP retrieval libraries utilized to harvest live web snippets and encyclopedia entries concurrently.</li>
    </ul>

    <h3>2.5.3 Frontend Technologies</h3>
    <ul>
      <li><b>HTML5 & CSS3:</b> Semantic structure styled with modern cyberpunk glassmorphic elements, backdrop filters, and custom scrollbars.</li>
      <li><b>Vanilla JavaScript (ES6+):</b> Asynchronous fetch API, multipart/form-data packaging, dynamic progress bar animations, and DOM rendering.</li>
    </ul>

    <h3>2.5.4 Integrated Development Environment (IDE)</h3>
    <p>The system was implemented and debugged using Visual Studio Code and Windows PowerShell.</p>
  </div>
</div>
""")

# PAGE 23: 2.5.5 VERSION CONTROL, TESTING & SECURITY
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">15</div>
    <h3>2.5.5 Version Control System</h3>
    <p>
      <b>Git & GitHub:</b> Used for collaborative code development, branch management, issue tracking, and version history preservation across all project milestones.
    </p>

    <h3>2.5.6 Testing & Debugging Tools</h3>
    <p>Rigorous testing ensured that neural embeddings, web scraping, and UI state updates functioned smoothly without memory leaks:</p>
    <ul>
      <li><b>Python Unittest & PyTest:</b> Automated unit testing of image normalization, token overlap, and score fusion functions.</li>
      <li><b>Postman & cURL:</b> REST API endpoint validation, boundary payload testing, and HTTP status code verification.</li>
      <li><b>Chrome DevTools:</b> Client-side DOM inspection, JavaScript console debugging, and network waterfall analysis.</li>
    </ul>

    <h3>2.5.7 Security Measures</h3>
    <p>Security and data integrity are fundamental to prevent system compromise and memory crashes:</p>
    <ol>
      <li>
        <b>File Upload Sanitization:</b> Incoming image names are filtered using <code>secure_filename()</code> to eliminate directory traversal sequences (e.g. <code>../../</code>).
      </li>
      <li>
        <b>Payload Capacity Protection:</b> Flask <code>MAX_CONTENT_LENGTH</code> is strictly capped at 100 MB to prevent Denial-of-Service attacks via oversized payloads.
      </li>
      <li>
        <b>Temporary Storage Cleanup:</b> All uploaded images are stored with unique UUID filenames in a dedicated temporary folder and deleted immediately after analysis via <code>safe_remove()</code> in a <code>finally</code> block.
      </li>
      <li>
        <b>Image File Signature Validation:</b> Image headers are verified using Pillow's binary verification before passing to neural models, blocking disguised scripts or non-image binaries.
      </li>
    </ol>
  </div>
</div>
""")

# PAGE 24: 2.6 SURVEY OF TECHNOLOGY (PART 1)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">16</div>
    <h2>2.6 SURVEY OF TECHNOLOGY</h2>
    <p>
      The selection of technologies for VERIFAI was based on cross-modal representation power, inference latency, security, and developer ergonomics:
    </p>

    <h3>2.6.1 Vision-Language Modeling – OpenAI CLIP (ViT-B/32)</h3>
    <p>The choice of CLIP is justified by several foundational advantages:</p>
    <ul>
      <li><b>Zero-Shot Transfer:</b> CLIP is pre-trained on 400 million (image, text) pairs. It matches open-vocabulary natural language claims without requiring fine-tuning on domain-specific datasets.</li>
      <li><b>Metric Embedding Space:</b> Both modalities are projected into a normalized 512-dimensional vector space, allowing instant cosine similarity computation via vector dot-products.</li>
      <li><b>Robustness to Semantic Shifts:</b> Shows superior resilience compared to standard ImageNet classifiers when presented with real-world news photos and graphical variations.</li>
    </ul>

    <h3>2.6.2 Image Captioning – Salesforce BLIP</h3>
    <p>BLIP (Bootstrapping Language-Image Pre-training) is chosen for:</p>
    <ul>
      <li><b>Natural Language Synthesis:</b> Converts photographic pixels into descriptive captions (e.g. "a high speed train on railway tracks"), enabling direct lexical overlap analysis.</li>
      <li><b>Lightweight Inference:</b> Executes conditional captioning in under 0.8 seconds on modern CPUs and under 0.2 seconds on GPUs.</li>
    </ul>

    <h3>2.6.3 Character Extraction – Tesseract OCR</h3>
    <p>Tesseract OCR provides:</p>
    <ul>
      <li><b>Text Extraction:</b> Discovers in-image textual clues such as road signs, vehicle numbers, newspaper banners, and timestamps.</li>
      <li><b>Location Disambiguation:</b> Critical for detecting when image placards mention one city while textual claims claim another.</li>
    </ul>
  </div>
</div>
""")

# PAGE 25: 2.6 SURVEY OF TECHNOLOGY (PART 2)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">17</div>
    <h3>2.6.4 Evidence Retrieval Technologies</h3>
    <p>VERIFAI utilizes a multi-engine retrieval strategy to ensure robust external grounding:</p>
    <ul>
      <li><b>DuckDuckGo HTML Search:</b> Provides real-time news headlines and journalistic articles without requiring costly commercial API keys or subscription limits.</li>
      <li><b>Wikipedia OpenSearch API:</b> Delivers rapid, structured encyclopedia entity summaries and official historical references.</li>
      <li><b>Google Fact Check Explorer API:</b> Queries certified fact-checking agencies (e.g. Snopes, PolitiFact, BOOM Live) for existing debunk records.</li>
    </ul>

    <h3>2.6.5 Asynchronous Multi-Threading – ThreadPoolExecutor</h3>
    <p>
      Python's <code>concurrent.futures.ThreadPoolExecutor</code> was selected to parallelize the verification workload. By dispatching OCR, CLIP/BLIP inference, and web evidence harvesting across 4 background threads, total response time was reduced from ~50 seconds down to 3.5–4.5 seconds.
    </p>

    <h3>Conclusion of Survey</h3>
    <p>
      The chosen technologies align with the project's goals of real-time performance, multimodal accuracy, and explainable evidence delivery. PyTorch and CLIP deliver state-of-the-art vision-language matching, Tesseract adds textual grounding, multi-threaded search ensures factual verification, and Flask provides a responsive, robust API backend.
    </p>
  </div>
</div>
""")

# PAGE 26: CHAPTER 3 - SYSTEM DESIGN (3.1 MODULE DIVISION)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">18</div>
    <h1>CHAPTER 3 SYSTEM DESIGN</h1>
    
    <h2>3.1 MODULE DIVISION :</h2>
    <p>
      The Multimodal Misinformation Verification System consists of five interconnected modules that handle user interaction, API orchestration, multimodal inference, evidence retrieval, and decision fusion:
    </p>

    <h3>3.1.1 User Interface Module</h3>
    <ul>
      <li><b>Claim Input & Image Dropzone:</b> Handles user textual assertions and accepts drag-and-drop file uploads across all standard formats.</li>
      <li><b>Dynamic Verification Dashboard:</b> Displays real-time progress animations, visual similarity meters, and expandable evidence citation cards.</li>
    </ul>

    <h3>3.1.2 API Orchestration Module (Flask REST Backend)</h3>
    <ul>
      <li><b>Request Handling & Sanitization:</b> Parses incoming multipart requests, verifies MIME types, and applies 100 MB limits.</li>
      <li><b>Thread Pool Dispatcher:</b> Manages <code>ThreadPoolExecutor(max_workers=4)</code> to execute inference, OCR, and search in parallel.</li>
      <li><b>Temporary Asset Management:</b> Generates unique UUID filenames and ensures file cleanup upon request completion.</li>
    </ul>

    <h3>3.1.3 Multimodal Vision-Language Module</h3>
    <ul>
      <li><b>CLIP Similarity Engine:</b> Computes cross-modal dot products and normalized cosine similarity scores.</li>
      <li><b>BLIP Caption Generator:</b> Generates descriptive visual sentences and computes stemmed word overlap.</li>
      <li><b>Contrastive Grounding:</b> Evaluates contradiction signals against unrelated distractor embeddings.</li>
    </ul>

    <h3>3.1.4 Evidence Retrieval Module</h3>
    <ul>
      <li><b>Multi-Provider Search:</b> Concurrently queries DuckDuckGo, Wikipedia, and Google Fact Check Explorer.</li>
      <li><b>Non-Empty Result Caching:</b> Caches validated search results to eliminate redundant network queries.</li>
    </ul>
  </div>
</div>
""")

# PAGE 27: 3.1.5 - 3.1.9 SYSTEM DESIGN MODULES
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">19</div>
    <h3>3.1.5 Evidence Fusion & Decision Engine</h3>
    <ul>
      <li><b>Calibrated Bayesian Scoring:</b> Synthesizes visual similarity (60%), caption overlap (20%), OCR match (10%), and metadata forensics (10%).</li>
      <li><b>Conflict Penalty Logic:</b> Applies immediate score penalties when location or entity contradictions are detected.</li>
      <li><b>Three-Tier Verdict Assignment:</b> Classifies queries into Likely Consistent (🟢), Potentially Misleading (🔴), or Needs Verification (🟡).</li>
    </ul>

    <h3>3.1.6 OCR & Forensic Analysis Module</h3>
    <ul>
      <li><b>Optical Character Recognition:</b> Utilizes Tesseract to read text placards, banners, and digital overlays.</li>
      <li><b>Metadata Forensics:</b> Inspects image dimensions, aspect ratios, file size, and EXIF camera parameters.</li>
    </ul>

    <h3>3.1.7 Location Disambiguation Heuristic</h3>
    <ul>
      <li><b>Geographical Entity Matching:</b> Compares location names extracted from OCR against claimed locations.</li>
      <li><b>Misattribution Trap:</b> Flags posts where photos depicting one city/country are falsely captioned as another.</li>
    </ul>

    <h3>3.1.8 System Security & Error Trapping</h3>
    <ul>
      <li><b>Input Sanitization:</b> Eliminates malicious filenames and caps memory buffers.</li>
      <li><b>Exception Isolation:</b> Ensures search timeouts or image processing glitches do not crash the Flask server.</li>
    </ul>
  </div>
</div>
""")

# PAGE 28: 3.2 GANTT CHART
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">20</div>
    <h2>3.2 GANTT CHART</h2>
    <p><b>Multimodal Misinformation Verification Development Timeline</b></p>

    <div class="diagram-box" style="text-align: left; font-size: 8.5pt;">
Phase                                Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar
-----------------------------------------------------------------------------
1. Literature Survey & Problem Def. [███]
2. Dataset Collection (Fakeddit)         [███]
3. Model Prototyping (CLIP/BLIP)              [████]
4. Evidence Pipeline Engineering                   [████]
5. Parallel Optimization & Speed                        [████]
6. Web Interface & System Testing                            [████]
7. Final Report & Viva Prep                                       [████]
    </div>

    <p style="margin-top: 15px;">
      The development lifecycle was structured into iterative academic sprints:
    </p>
    <ul>
      <li><b>Sprint 1 (Aug - Sep):</b> Analysis of cheapfakes, survey of visual-language models, and exploration of the Fakeddit dataset.</li>
      <li><b>Sprint 2 (Oct - Nov):</b> Implementation of CLIP ViT-B/32 and BLIP captioning pipelines in PyTorch.</li>
      <li><b>Sprint 3 (Dec - Jan):</b> Engineering of asynchronous evidence retrieval via DuckDuckGo and Wikipedia OpenSearch.</li>
      <li><b>Sprint 4 (Feb - Mar):</b> Thread pooling optimization, 100MB format support, comprehensive testing, and Black Book preparation.</li>
    </ul>
  </div>
</div>
""")

# PAGE 29: 3.3 E-R DIAGRAM
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">21</div>
    <h2>3.3 E-R DIAGRAM</h2>
    <p>This diagram represents the entities and relationships in the verification session data:</p>

    <div class="diagram-box">
┌───────────────────────┐          ┌───────────────────────┐
│   VERIFICATION_LOG    │          │    EVIDENCE_SOURCE    │
├───────────────────────┤ 1      N ├───────────────────────┤
│ response_id (PK)      │◄─────────┤ source_id (PK)        │
│ claim_text            │          │ response_id (FK)      │
│ image_name            │          │ title                 │
│ clip_score            │          │ snippet               │
│ blip_caption          │          │ url                   │
│ ocr_text              │          │ domain                │
│ final_verdict         │          │ relevance_score       │
│ latency_seconds       │          └───────────────────────┘
│ timestamp             │
└───────────────────────┘
    </div>

    <p><b>Entities & Relationships Description:</b></p>
    <ul>
      <li><b>VERIFICATION_LOG:</b> Stores metadata for each verification request, including unique response ID, claim text, image filename, computed similarity scores, generated captions, final verdict, and latency.</li>
      <li><b>EVIDENCE_SOURCE:</b> Represents individual retrieved web citations associated with a verification session, linked via foreign key (response_id). Stores title, snippet, publisher domain, and URL.</li>
    </ul>
  </div>
</div>
""")

# PAGE 30: 3.4 DATA FLOW REPRESENTATION
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">22</div>
    <h2>3.4 DATA FLOW REPRESENTATION</h2>
    
    <h3>3.4.1 DATA FLOW DIAGRAM</h3>
    <p>Data Flow Representation describes how data moves through the VERIFAI platform, ensuring efficient processing and communication between modules:</p>

    <div class="diagram-box">
Level 0 DFD (Context Diagram):
             [Claim Text + Photo Upload]
  ┌──────┐ ──────────────────────────────► ┌───────────────────────────┐
  │ User │                                 │ 0.0 VERIFAI Multimodal    │
  │      │ ◄────────────────────────────── │     Verification Engine   │
  └──────┘    [Verdict + 5 Evidence Links] └─────────────┬─────────────┘
                                                         │ Search Query
                                                         ▼
                                           ┌───────────────────────────┐
                                           │ Web Evidence Data Sources │
                                           └───────────────────────────┘

Level 1 DFD (Decomposition):
  [Claim] ───────► (1.0 Preprocess Claim) ──► (3.0 CLIP Text Encoder)
                          │                          │
                          ▼                          ▼
                   (5.0 Web Retrieval)       (6.0 Cross-Modal Math)
                          │                          ▲
  [Image] ───────► (2.0 Image Resizer) ────► (4.0 CLIP Visual Encoder)
                          │
                          ├────────────────► (7.0 BLIP Captioning)
                          │
                          └────────────────► (8.0 Tesseract OCR)
                                                     │
                                                     ▼
                                            (9.0 Evidence Fusion) ──► [Verdict]
    </div>
  </div>
</div>
""")

# PAGE 31: 3.5 UML DIAGRAMS (3.5.1 CLASS DIAGRAM)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">23</div>
    <h2>3.5 UML DIAGRAMS</h2>
    
    <h3>3.5.1 CLASS DIAGRAM</h3>
    <p>This class diagram represents the structural architecture of the backend Python classes and services:</p>

    <div class="diagram-box" style="text-align: left;">
┌─────────────────────────────────┐       ┌────────────────────────────────┐
│         AppController           │       │          AIVerifier            │
├─────────────────────────────────┤       ├────────────────────────────────┤
│ - upload_dir: String            │       │ - clip_model: CLIPModel        │
│ - max_file_size: Integer (100MB)│       │ - clip_proc: CLIPProcessor     │
├─────────────────────────────────┤       │ - blip_model: BlipForCondGen   │
│ + verify(): Response            │       ├────────────────────────────────┤
│ + allowed_file(): Boolean       │       │ + check_consistency(): Dict    │
│ + safe_remove(): Void           │       │ + calculate_visual(): Dict     │
└────────────────┬────────────────┘       │ + generate_caption(): String   │
                 │                        └────────────────────────────────┘
                 ▼                                        ▲
┌─────────────────────────────────┐                       │
│        EvidenceRetriever        │───────────────────────┘
├─────────────────────────────────┤
│ - cache: Dict                   │
├─────────────────────────────────┤
│ + search_evidence(): List       │
│ + search_ddg(): List            │
│ + search_wikipedia(): List      │
└─────────────────────────────────┘
    </div>

    <p><b>Class Descriptions:</b></p>
    <ul>
      <li><b>AppController:</b> Manages HTTP requests, file uploads, thread pooling, and JSON responses.</li>
      <li><b>AIVerifier:</b> Loads and executes OpenAI CLIP and Salesforce BLIP foundation models.</li>
      <li><b>EvidenceRetriever:</b> Handles multi-threaded web queries across search engines with fallback caching.</li>
    </ul>
  </div>
</div>
""")

# PAGE 32: 3.5.2 SEQUENCE DIAGRAM
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">24</div>
    <h3>3.5.2 SEQUENCE DIAGRAM</h3>
    <p>This diagram depicts the chronological interaction sequence between user, frontend, backend API, neural models, and web search engines:</p>

    <div class="diagram-box" style="text-align: left;">
User           Web Frontend            Flask Backend         CLIP & BLIP       Web Search
 │                  │                        │                    │                 │
 │── Submit Post ──►│                        │                    │                 │
 │                  │── POST /verify ───────►│                    │                 │
 │                  │                        │── Compute Tensors ►│                 │
 │                  │                        │── Query Evidence ───────────────────►│
 │                  │                        │◄── Cosine Scores ──│                 │
 │                  │                        │◄── 5 Web Sources ────────────────────│
 │                  │                        │ [Run Fusion Engine]│                 │
 │                  │◄── Return JSON ────────│                    │                 │
 │◄─ Display Verdict│    (Score & Sources)   │                    │                 │
    </div>

    <p><b>Sequence Steps:</b></p>
    <ol>
      <li><b>Submit Post:</b> User enters a claim and uploads a photograph on the web interface.</li>
      <li><b>POST Request:</b> Frontend packages inputs into a multipart/form-data request to <code>/verify</code>.</li>
      <li><b>Concurrent Inference:</b> Flask backend dispatches concurrent tasks to CLIP/BLIP and Web Search.</li>
      <li><b>Result Aggregation:</b> Backend combines vision similarity, OCR text, and web citations into a calibrated verdict.</li>
      <li><b>UI Update:</b> Frontend renders the final result, meters, and citations dynamically.</li>
    </ol>
  </div>
</div>
""")

# PAGE 33: 3.5.3 STATE CHART DIAGRAM
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">25</div>
    <h3>3.5.3 STATE CHART DIAGRAM</h3>
    <p>This diagram illustrates the lifecycle states of a verification transaction:</p>

    <div class="diagram-box">
  [State: Idle / Waiting]
        │
        ▼ (User uploads Image & Claim)
  [State: Input Validation] ──── (Invalid / Empty) ───► [State: Error 400]
        │ (Valid Input)
        ▼
  [State: Parallel Inference & Search]
        │ (Extract CLIP, BLIP, OCR & Web Search concurrently)
        ▼
  [State: Evidence Fusion & Conflict Check]
        │
        ├─ High Alignment (Score ≥ 60%) ────► [State: Likely Consistent (🟢)]
        ├─ Location / Semantic Mismatch ────► [State: Potentially Misleading (🔴)]
        └─ Inconclusive Evidence ───────────► [State: Needs Verification (🟡)]
        │
        ▼
  [State: Clean Temporary File & Return JSON Response]
    </div>

    <p><b>State Explanations:</b></p>
    <ul>
      <li><b>Idle State:</b> System awaits user input on port 5500.</li>
      <li><b>Validation State:</b> Verifies image format and payload size (&lt;100MB).</li>
      <li><b>Parallel Inference State:</b> Multi-threaded execution across neural models and web search engines.</li>
      <li><b>Decision States:</b> Categorizes output into Consistent, Misleading, or Needs Verification.</li>
    </ul>
  </div>
</div>
""")

# PAGE 34: 3.5.4 USE-CASE DIAGRAM
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">26</div>
    <h3>3.5.4 USE-CASE DIAGRAM</h3>
    <p>This diagram models the functional capabilities available to users interacting with the system:</p>

    <div class="diagram-box" style="text-align: left;">
             ┌────────────────────────────────────────────────────────┐
             │            VERIFAI Multimodal Fact-Checker             │
             │                                                        │
             │   (Upload Image - JPG/PNG/JFIF/AVIF) ◄──────┐          │
             │                                             │          │
  ┌──────┐   │   (Input Text Claim Statement) ◄────────────┤          │
  │ User ├───┤                                             ├── [User] │
  │      │   │   (View Authenticity Verdict) ◄─────────────┤          │
  └──────┘   │                                             │          │
             │   (Inspect Metric Meters & BLIP Caption) ◄──┤          │
             │                                             │          │
             │   (Click Verified Primary Web Sources) ◄────┘          │
             └────────────────────────────────────────────────────────┘
    </div>

    <p><b>Actors & Use Cases:</b></p>
    <ul>
      <li><b>User / Fact-Checker:</b> Submits claim, uploads image, inspects visual-text alignment meters, reviews OCR detections, and accesses primary fact-check links.</li>
      <li><b>Use Cases:</b> Image Upload, Claim Input, Multimodal Verification, Evidence Citation Review, and Forensic Metadata Inspection.</li>
    </ul>
  </div>
</div>
""")

# PAGE 35: CHAPTER 4 - IMPLEMENTATION & TESTING (4.1 CODE - PART 1)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">27</div>
    <h1>CHAPTER 4 IMPLEMENTATION AND TESTING</h1>
    
    <h2>4.1 CODE :</h2>
    <p><b>Module 1: Flask Multi-Threaded Verification REST API (Backend/app.py)</b></p>

    <div class="code-container">
<span class="kw">@app.post</span>(<span class="str">"/verify"</span>)
<span class="kw">def</span> <span class="fn">verify</span>():
    response_id = <span class="str">"VER-"</span> + uuid.uuid4().hex[:<span class="num">10</span>].upper()
    claim = request.form.get(<span class="str">"claim"</span>, <span class="str">""</span>).strip()
    image = request.files.get(<span class="str">"image"</span>)

    <span class="kw">if not</span> claim <span class="kw">or not</span> image:
        <span class="kw">return</span> jsonify({<span class="str">"status"</span>: <span class="str">"error"</span>, <span class="str">"error"</span>: <span class="str">"Claim and image required."</span>}), <span class="num">400</span>

    original_name = secure_filename(image.filename) <span class="kw">or</span> <span class="str">"upload.jpg"</span>
    image_path = os.path.join(UPLOAD_FOLDER, f<span class="str">"{{uuid.uuid4().hex}}_{{original_name}}"</span>)
    image.save(image_path)

    <span class="com"># Universal format normalization and auto-downscale</span>
    <span class="kw">try</span>:
        <span class="kw">with</span> PILImage.open(image_path) <span class="kw">as</span> im:
            im.load()
            <span class="kw">if</span> max(im.size) > <span class="num">1600</span>:
                im.thumbnail((<span class="num">1600</span>, <span class="num">1600</span>), PILImage.Resampling.LANCZOS)
            <span class="kw">if</span> im.mode != <span class="str">"RGB"</span>:
                im = im.convert(<span class="str">"RGB"</span>)
            im.save(image_path, <span class="str">"JPEG"</span>, quality=<span class="num">90</span>)
    <span class="kw">except</span> Exception <span class="kw">as</span> err:
        logger.warning(f<span class="str">"Image optimization note: {{err}}"</span>)

    <span class="com"># Multi-threaded parallel execution across 4 background workers</span>
    <span class="kw">with</span> ThreadPoolExecutor(max_workers=<span class="num">4</span>) <span class="kw">as</span> executor:
        future_ocr = executor.submit(extract_text, image_path)
        future_ver = executor.submit(check_consistency, claim, image_path, <span class="str">""</span>, metadata)
        future_trn = executor.submit(predict_trained_model, claim, image_path)
        future_evd = executor.submit(search_evidence, claim)

        extracted_text = future_ocr.result()
        result = future_ver.result()
        evidence = future_evd.result()

    <span class="kw">return</span> jsonify({<span class="str">"status"</span>: <span class="str">"success"</span>, <span class="str">"result"</span>: result[<span class="str">"result"</span>], <span class="str">"evidence"</span>: evidence})
    </div>
  </div>
</div>
""")

# PAGE 36: 4.1 CODE - PART 2
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">28</div>
    <p><b>Module 2: Vision-Language Alignment & Captioning (Backend/ai_verifier.py)</b></p>

    <div class="code-container">
<span class="kw">@lru_cache</span>(maxsize=<span class="num">1</span>)
<span class="kw">def</span> <span class="fn">load_clip</span>():
    processor = CLIPProcessor.from_pretrained(<span class="str">"openai/clip-vit-base-patch32"</span>)
    model = CLIPModel.from_pretrained(<span class="str">"openai/clip-vit-base-patch32"</span>).to(DEVICE)
    model.eval()
    <span class="kw">return</span> processor, model

<span class="kw">@lru_cache</span>(maxsize=<span class="num">1</span>)
<span class="kw">def</span> <span class="fn">load_blip</span>():
    processor = BlipProcessor.from_pretrained(<span class="str">"Salesforce/blip-image-captioning-base"</span>)
    model = BlipForConditionalGeneration.from_pretrained(<span class="str">"Salesforce/blip-image-captioning-base"</span>).to(DEVICE)
    model.eval()
    <span class="kw">return</span> processor, model

<span class="kw">def</span> <span class="fn">calculate_visual_signal</span>(claim, image_path, image_caption):
    processor, model = load_clip()
    image = Image.open(image_path).convert(<span class="str">"RGB"</span>)
    distractor = <span class="str">"an unrelated random object with no contextual connection"</span>

    <span class="com"># Contrastive grounding over 3 propositions</span>
    inputs = processor(
        text=[claim, image_caption, distractor],
        images=image,
        return_tensors=<span class="str">"pt"</span>,
        padding=<span class="kw">True</span>
    ).to(DEVICE)

    <span class="kw">with</span> torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=<span class="num">1</span>).cpu().numpy()[<span class="num">0</span>]

    grounded_match = float(probs[<span class="num">0</span>] * <span class="num">100.0</span>)
    contradiction_score = float(probs[<span class="num">2</span>] * <span class="num">100.0</span>)
    <span class="kw">return</span> {<span class="str">"grounded_match"</span>: grounded_match, <span class="str">"contradiction"</span>: contradiction_score}
    </div>
  </div>
</div>
""")

# PAGE 37: 4.1 CODE - PART 3
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">29</div>
    <p><b>Module 3: Multi-Source Web Evidence Retrieval (Backend/evidence_retrieval.py)</b></p>

    <div class="code-container">
<span class="kw">def</span> <span class="fn">search_evidence</span>(claim):
    clean_query = clean_search_query(claim)
    <span class="kw">if</span> clean_query <span class="kw">in</span> _CACHE:
        <span class="kw">return</span> _CACHE[clean_query]

    results = []
    <span class="com"># Multi-threaded concurrent web queries</span>
    <span class="kw">with</span> ThreadPoolExecutor(max_workers=<span class="num">3</span>) <span class="kw">as</span> executor:
        f_ddg = executor.submit(search_ddg_concurrent, clean_query)
        f_wiki = executor.submit(search_wikipedia_opensearch, clean_query)
        f_fact = executor.submit(search_factcheck_explorer, clean_query)

        <span class="kw">try</span>:
            results.extend(f_ddg.result(timeout=<span class="num">4.5</span>))
        <span class="kw">except</span> Exception:
            <span class="kw">pass</span>

        <span class="kw">try</span>:
            results.extend(f_wiki.result(timeout=<span class="num">3.5</span>))
        <span class="kw">except</span> Exception:
            <span class="kw">pass</span>

    <span class="com"># Deduplicate by domain and format top 4-5 citations</span>
    seen_domains = set()
    filtered = []
    <span class="kw">for</span> item <span class="kw">in</span> results:
        domain = item.get(<span class="str">"domain"</span>, <span class="str">""</span>)
        <span class="kw">if</span> domain <span class="kw">not in</span> seen_domains:
            seen_domains.add(domain)
            filtered.append(item)
        <span class="kw">if</span> len(filtered) >= <span class="num">5</span>:
            <span class="kw">break</span>

    <span class="kw">if</span> len(filtered) >= <span class="num">4</span>:
        _CACHE[clean_query] = filtered
    <span class="kw">return</span> filtered
    </div>
  </div>
</div>
""")

# PAGE 38: 4.1 CODE - PART 4
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">30</div>
    <p><b>Module 4: Evidence Fusion & Location Conflict (Backend/evidence_fusion.py)</b></p>

    <div class="code-container">
<span class="kw">def</span> <span class="fn">combine_verification_scores</span>(multimodal_score, evidence_sources):
    <span class="kw">if not</span> evidence_sources:
        evidence_score = <span class="num">50.0</span>
        confidence = <span class="str">"Medium"</span>
    <span class="kw">else</span>:
        relevance_values = [s.get(<span class="str">"relevance"</span>, <span class="num">70.0</span>) <span class="kw">for</span> s <span class="kw">in</span> evidence_sources]
        evidence_score = sum(relevance_values) / len(relevance_values)
        confidence = <span class="str">"High"</span>

    <span class="com"># Weighted synthesis: 70% Multimodal Visual-Text, 30% Web Evidence</span>
    combined = (multimodal_score * <span class="num">0.70</span>) + (evidence_score * <span class="num">0.30</span>)
    combined = round(max(<span class="num">0.0</span>, min(<span class="num">100.0</span>, combined)), <span class="num">2</span>)

    <span class="kw">if</span> combined >= <span class="num">65.0</span>:
        decision = <span class="str">"Likely Consistent"</span>
    <span class="kw">elif</span> combined <= <span class="num">35.0</span>:
        decision = <span class="str">"Potentially Misleading"</span>
    <span class="kw">else</span>:
        decision = <span class="str">"Needs Verification"</span>

    <span class="kw">return</span> {
        <span class="str">"combined_score"</span>: combined,
        <span class="str">"decision"</span>: decision,
        <span class="str">"confidence"</span>: confidence,
        <span class="str">"source_count"</span>: len(evidence_sources)
    }
    </div>
  </div>
</div>
""")

# PAGE 39: 4.2 TESTING APPROACH
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">30</div>
    <h2>4.2 TESTING APPROACH</h2>
    <p>
      The verification pipeline was systematically evaluated using unit testing, integration testing, and adversarial stress testing.
    </p>

    <h3>4.2.1 Unit Testing</h3>
    <p>Unit testing focused on verifying the correctness of individual components in isolation:</p>
    <ul>
      <li><b>CLIP Tensor Calculations:</b> Verified normalized vector dot-products and softmax consistency.</li>
      <li><b>BLIP Captioning:</b> Evaluated accuracy of generated descriptions on standard COCO images.</li>
      <li><b>OCR Extraction:</b> Validated text recognition accuracy on clear and degraded image banners.</li>
      <li><b>File Normalization:</b> Tested automatic conversion of .jfif and .avif images to RGB JPEG.</li>
    </ul>

    <h3>4.2.2 Integration Testing</h3>
    <p>Integration testing ensured seamless data flow between the frontend UI, Flask backend, neural models, and web search engines:</p>
    <ul>
      <li><b>Full-Stack Communication:</b> Validated multipart form submissions from JavaScript fetch to Flask.</li>
      <li><b>Concurrent Thread Pooling:</b> Verified that 4 worker threads operate concurrently without thread contention.</li>
      <li><b>Evidence Fusion:</b> Checked that combined scores correctly reflect both multimodal alignment and web sources.</li>
    </ul>

    <h3>4.3 Testing Tools</h3>
    <table>
      <thead>
        <tr><th>Tool</th><th>Purpose</th></tr>
      </thead>
      <tbody>
        <tr><td>PyTest</td><td>Automated unit testing of image normalization and scoring functions</td></tr>
        <tr><td>Postman & cURL</td><td>API endpoint verification, boundary testing, and HTTP status checks</td></tr>
        <tr><td>Chrome DevTools</td><td>Frontend DOM inspection, network latency analysis, and meter rendering</td></tr>
        <tr><td>Python cProfile</td><td>Profiling execution bottlenecks and optimizing model inference times</td></tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 40: 4.4 EXPECTED OUTCOMES & 4.5 TEST ENVIRONMENT
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">31</div>
    <h2>4.4 Expected Outcomes</h2>
    <ol>
      <li><b>Authentic Claims:</b> Legitimate claims paired with correct images should yield &gt;75% similarity and 'Likely Consistent' verdict.</li>
      <li><b>Misattributed Claims:</b> Out-of-context claims should yield &lt;30% similarity and 'Potentially Misleading' verdict.</li>
      <li><b>Location Conflicts:</b> Inconsistencies between claimed and detected locations must trigger immediate warning penalties.</li>
      <li><b>Evidence Quantity:</b> Every query must return 4 to 5 verified web sources with titles and clickable URLs.</li>
      <li><b>Latency:</b> End-to-end processing time must remain under 4.5 seconds.</li>
    </ol>

    <h2>4.5 Test Environment</h2>
    <table>
      <thead>
        <tr><th>Component</th><th>Details</th></tr>
      </thead>
      <tbody>
        <tr><td>Operating System</td><td>Microsoft Windows 11 (64-bit)</td></tr>
        <tr><td>Python Runtime</td><td>Python 3.11 64-bit</td></tr>
        <tr><td>Deep Learning Framework</td><td>PyTorch 2.4 (CPU / CUDA)</td></tr>
        <tr><td>Transformers Library</td><td>Hugging Face Transformers 4.40+</td></tr>
        <tr><td>Web Framework</td><td>Flask 3.0.2 / Werkzeug</td></tr>
        <tr><td>Test Hardware</td><td>Intel Core i5 (2.5 GHz), 16 GB DDR4 RAM, 512 GB SSD</td></tr>
      </tbody>
    </table>

    <h2>4.6 Tested Features</h2>
    <table>
      <thead>
        <tr><th>Feature</th><th>Test Case ID</th><th>Status</th></tr>
      </thead>
      <tbody>
        <tr><td>Visual-Text Semantic Alignment</td><td>TC_01</td><td>Passed</td></tr>
        <tr><td>Out-of-Context News Misattribution</td><td>TC_02</td><td>Passed</td></tr>
        <tr><td>Location Contradiction Flagging</td><td>TC_03</td><td>Passed</td></tr>
        <tr><td>Universal Object Categorization</td><td>TC_04</td><td>Passed</td></tr>
        <tr><td>JFIF / AVIF Image Format Ingestion</td><td>TC_05</td><td>Passed</td></tr>
        <tr><td>Multi-Source Evidence Retrieval</td><td>TC_06</td><td>Passed</td></tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 41: 4.7 TEST CASE DETAILS (PART 1)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">32</div>
    <h2>4.7 Test Case Details</h2>
    
    <p><b>News Misattribution & Cross-Modal Testing:</b></p>
    <table>
      <thead>
        <tr>
          <th>Test ID</th>
          <th>Scenario</th>
          <th>Test Steps</th>
          <th>Expected Output</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>TC_01.1</td>
          <td>Real News Claim</td>
          <td>1. Upload vande_bharat_train.jpg<br>2. Enter "Vande Bharat semi high speed train in India"<br>3. Click Analyze</td>
          <td>Likely Consistent (Score: 89.99%, 5 sources)</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_01.2</td>
          <td>Fabricated Context</td>
          <td>1. Upload vande_bharat_train.jpg<br>2. Enter "Underwater bullet train in Dubai desert"<br>3. Click Analyze</td>
          <td>Potentially Misleading (Score: 19.3%, 5 sources)</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_02.1</td>
          <td>Geographical Contradiction</td>
          <td>1. Upload taj_mahal_agra.jpg<br>2. Enter "Royal Buckingham Palace in London UK"<br>3. Click Analyze</td>
          <td>Potentially Misleading (Score: 4.99%, 5 sources)</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_02.2</td>
          <td>Authentic Landmark</td>
          <td>1. Upload taj_mahal_agra.jpg<br>2. Enter "The Taj Mahal white marble mausoleum in Agra"<br>3. Click Analyze</td>
          <td>Likely Consistent (Score: 66.32%, 5 sources)</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_03.1</td>
          <td>Aerospace Assertion</td>
          <td>1. Upload isro_rocket_launch.jpg<br>2. Enter "ISRO PSLV rocket launching into space"<br>3. Click Analyze</td>
          <td>Likely Consistent (Score: 78.55%, 5 sources)</td>
          <td>Passed</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 42: 4.7 TEST CASE DETAILS (PART 2)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">33</div>
    <p><b>Universal Object Categories & Format Handling Testing:</b></p>

    <table>
      <thead>
        <tr>
          <th>Test ID</th>
          <th>Scenario</th>
          <th>Test Steps</th>
          <th>Expected Output</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>TC_04.1</td>
          <td>Automobile Verification</td>
          <td>1. Upload bmw_car.jpg<br>2. Enter "A luxury BMW sedan car parked outdoors"<br>3. Click Analyze</td>
          <td>Likely Consistent (Score: 88.5%, 5 sources)</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_04.2</td>
          <td>Animal Verification</td>
          <td>1. Upload cat_animal.jpg<br>2. Enter "A cute domestic cat sitting on the floor"<br>3. Click Analyze</td>
          <td>Likely Consistent (Score: 84.2%, 5 sources)</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_05.1</td>
          <td>JFIF Format Handling</td>
          <td>1. Upload download.jfif from Chrome<br>2. Enter "is this photo shows CEO of corbion company"<br>3. Click Analyze</td>
          <td>Status 200 OK (Processed in 3.58s, No 400 error)</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_05.2</td>
          <td>100MB File Handling</td>
          <td>1. Upload high-res 4K camera photo<br>2. Enter valid descriptive claim<br>3. Click Analyze</td>
          <td>Auto-downscaled to 1600px, processed without crash</td>
          <td>Passed</td>
        </tr>
        <tr>
          <td>TC_06.1</td>
          <td>Evidence Retrieval</td>
          <td>1. Submit any news assertion<br>2. Check returned evidence list</td>
          <td>4 to 5 clickable citations with title, domain, snippet</td>
          <td>Passed</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 43: CHAPTER 5 - RESULTS AND DISCUSSIONS (FIGURE 5.1 & 5.2)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">34</div>
    <h1>CHAPTER 5 RESULTS AND DISCUSSIONS</h1>
    
    <h2>5.1 FUNCTIONALITY EVALUATION</h2>
    <p><b>VERIFAI System Output Dashboard:</b></p>

    <img src="{ss1_path}" alt="VERIFAI Dashboard Screenshot 1" class="screenshot-img">
    <p class="text-center" style="font-size: 9.5pt; font-style: italic; margin-top: 4px;">Figure 5.1: VERIFAI Live Web Interface verifying multimodal claim with real-time meters and supporting citations.</p>

    <div class="diagram-box" style="text-align: left; font-size: 8.5pt;">
Audit Log Summary:
  - Input: vande_bharat_train.jpg (RGB Normalized)
  - Claim: "Vande Bharat Express semi high speed train running on Indian Railways"
  - Verdict: LIKELY CONSISTENT (🟢)
  - CLIP Similarity: 89.99% | BLIP Overlap: 25.0% | Processing Latency: 3.58s
  - Evidence Citations: 5 Verified Sources (Wikipedia, Ixigo, IRCTC, etc.)
    </div>
  </div>
</div>
""")

# PAGE 44: CHAPTER 5 - SYSTEM OUTPUT (FIGURE 5.3 & 5.4)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">35</div>
    <p><b>Consistent vs Misleading News Verification Outputs:</b></p>

    <img src="{ss2_path}" alt="VERIFAI Dashboard Screenshot 2" class="screenshot-img">
    <p class="text-center" style="font-size: 9.5pt; font-style: italic; margin-top: 4px;">Figure 5.2: Verification Output showing Mismatch Detection and Potentially Misleading verdict for out-of-context claims.</p>

    <p style="margin-top: 10px;">
      When an out-of-context claim is submitted (such as claiming a domestic railway train is an underwater Dubai bullet train), the visual similarity drops significantly below the consistency threshold. The system flags the mismatch with an explanatory note and cites verified web sources debulking the claim.
    </p>
  </div>
</div>
""")

# PAGE 45: CHAPTER 5 - EVIDENCE BREAKDOWN (FIGURE 5.5)
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">36</div>
    <p><b>Evidence Citations & Metadata Forensic Breakdown:</b></p>

    <img src="{ss3_path}" alt="VERIFAI Dashboard Screenshot 3" class="screenshot-img">
    <p class="text-center" style="font-size: 9.5pt; font-style: italic; margin-top: 4px;">Figure 5.3: Supporting Evidence List displaying titles, snippets, publisher domains, and direct hyperlinks.</p>

    <p style="margin-top: 10px;">
      The evidence section presents users with verified corroborating citations from high-authority encyclopedic and news domains (e.g., Wikipedia, official government releases, established news outlets). Users can directly click any citation to inspect the primary source in a new browser tab.
    </p>
  </div>
</div>
""")

# PAGE 46: 5.1 FEATURE IMPLEMENTATION & TESTING SUMMARY
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">38</div>
    <h2>1. Development and Feature Implementation</h2>
    <p>
      The Multimodal Misinformation Verification System was developed using Python, PyTorch, and Transformers for the backend AI engine, and HTML5, CSS3, and JavaScript for the frontend to ensure real-time verification functionality. The system provides an explainable verification experience with visual meters, OCR extraction, and multi-source evidence citations.
    </p>

    <h3>Key Features Implemented:</h3>
    <ul>
      <li><b>Multimodal Synchronization:</b> Real-time visual-text alignment and cosine similarity scoring.</li>
      <li><b>Scene Captioning:</b> BLIP descriptive captioning and stemmed n-gram lexical overlap.</li>
      <li><b>OCR & Location Checks:</b> Text banner extraction to flag geographical misattributions.</li>
      <li><b>Evidence Retrieval:</b> Asynchronous multi-threaded queries returning 4 to 5 verified citations.</li>
      <li><b>Format Ingestion:</b> Full support for JPG, PNG, WEBP, JFIF, and AVIF up to 100 MB.</li>
    </ul>

    <h2>2. Testing Results</h2>
    <table>
      <thead>
        <tr><th>Feature</th><th>Test Case ID</th><th>Status</th></tr>
      </thead>
      <tbody>
        <tr><td>User Input Processing</td><td>TC_01</td><td>Passed</td></tr>
        <tr><td>Image Validation & Normalization</td><td>TC_02</td><td>Passed</td></tr>
        <tr><td>CLIP Similarity Computation</td><td>TC_03</td><td>Passed</td></tr>
        <tr><td>Evidence Retrieval & Citations</td><td>TC_04</td><td>Passed</td></tr>
        <tr><td>Decision & Score Calibration</td><td>TC_05</td><td>Passed</td></tr>
        <tr><td>UI Dynamic Meters & Alerts</td><td>TC_06</td><td>Passed</td></tr>
      </tbody>
    </table>
  </div>
</div>
""")

# PAGE 47: 5.2 USER EXPERIENCE & DEFECT SUMMARY
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">39</div>
    <h3>Defect Summary for Progress Tracking:</h3>
    <table>
      <thead>
        <tr>
          <th>Defect ID</th>
          <th>Description</th>
          <th>Severity</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>D_01</td><td>10 MB file upload limit caused 413 Request Entity Too Large on high-res photos</td><td>Medium</td><td>Fixed</td></tr>
        <tr><td>D_02</td><td>Browser .jfif and .avif images rejected with 400 Bad Request</td><td>High</td><td>Fixed</td></tr>
        <tr><td>D_03</td><td>Evidence sources intermittently dropped to 0 due to scraper timeout</td><td>Medium</td><td>Fixed</td></tr>
      </tbody>
    </table>

    <h2>3. User Feedback</h2>
    <p>
      The system was evaluated by peer reviewers and test users to gather feedback on usability and speed.
    </p>
    <p><b>User Feedback Highlights:</b></p>
    <ul>
      <li>Users praised the fast response time (~3.5 seconds) compared to earlier versions (~50s).</li>
      <li>Visual similarity and OCR meters provided clear, transparent explainability.</li>
      <li>Verified citations with clickable links significantly increased user confidence in verdicts.</li>
    </ul>

    <p><b>Suggestions for Improvement:</b></p>
    <ul>
      <li>Add support for video stream verification (e.g. YouTube Shorts, Instagram Reels).</li>
      <li>Integrate multilingual support for regional Indic languages (Hindi, Marathi).</li>
    </ul>
  </div>
</div>
""")

# PAGE 48: CHAPTER 6 - CONCLUSION AND FUTURE WORK
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">40</div>
    <h1>CHAPTER 6 : CONCLUSION AND FUTURE WORK</h1>
    
    <h2>6.1 Conclusion</h2>
    <p>
      The Multimodal Misinformation Verification System project marks a significant step forward in the digital fact-checking landscape, delivering an explainable and reliable verification experience. With real-time visual-language alignment, descriptive captioning, location conflict detection, and multi-source evidence retrieval, the system provides a robust environment to counter out-of-context misattributions. Through careful design, development, and rigorous testing, the project successfully meets its core objectives, offering a smooth and engaging user experience.
    </p>

    <p>
      A major achievement of this project is its strong focus on real-time multimodal synchronization and performance optimization. By leveraging OpenAI CLIP for zero-shot contrastive grounding and Flask with 4-worker thread pooling, the system ensures sub-4-second query latencies while maintaining transparent citations. The intuitive UI/UX design enhances accessibility, allowing users to inspect visual similarity meters and open primary fact-check sources.
    </p>

    <p>
      However, the project does have some limitations, such as linguistic ambiguity in satirical posts and dependency on open-web search availability. Despite these challenges, these limitations present valuable opportunities for further research into fine-grained multimodal reasoning and multilingual knowledge graphs.
    </p>

    <h2>6.2 Future Scope</h2>
    <ul>
      <li><b>Video Verification:</b> Extend the architecture to verify video keyframes and audio tracks.</li>
      <li><b>Multilingual Encoders:</b> Incorporate multilingual foundation models (e.g. mCLIP, IndicBERT).</li>
      <li><b>Knowledge Graph Integration:</b> Construct persistent graphs of recurring visual hoaxes.</li>
    </ul>
  </div>
</div>
""")

# PAGE 49: 6.3 LIMITATIONS
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">41</div>
    <h2>6.3 Limitations</h2>
    <p>
      While the Multimodal Misinformation Verification System delivers a high-quality verification experience, certain limitations must be acknowledged:
    </p>

    <p><b>Potential Constraints:</b></p>
    <ul>
      <li><b>Satire and Irony:</b> Sarcastic captions paired with genuine imagery can sometimes trigger false-positive mismatch signals due to literal semantic differences.</li>
      <li><b>Abstract & Memetic Media:</b> Symbolic cartoons and memes lack literal visual features matching real-world factual claims.</li>
      <li><b>Search Rate Limits:</b> Heavy burst traffic from multiple users may occasionally encounter search engine rate limits without proxy rotation.</li>
      <li><b>Hardware Resource Demands:</b> Initial loading of transformer weights requires sufficient RAM (min 8 GB) during server startup.</li>
      <li><b>Offline Accessibility:</b> The evidence retrieval engine requires an active internet connection to query live web sources.</li>
    </ul>
  </div>
</div>
""")

# PAGE 50: CHAPTER 7 - REFERENCES
pages.append(f"""
<div class="page">
  <div class="page-border">
    <div class="top-page-num">42</div>
    <h1>CHAPTER 7 REFERENCES</h1>
    
    <p>For the Multimodal Misinformation Verification System project, the following references and resources were utilized:</p>
    
    <p><b>Websites and Online Resources:</b></p>
    <p>
      [1] <b>OpenAI CLIP Documentation</b><br>
      Comprehensive guide for implementing zero-shot contrastive vision-language representation.<br>
      Available at: <a href="https://github.com/openai/CLIP">https://github.com/openai/CLIP</a>
    </p>
    <p>
      [2] <b>Hugging Face Transformers Documentation</b><br>
      Official reference for transformer pipelines, tokenizers, and PyTorch model architectures.<br>
      Available at: <a href="https://huggingface.co/docs/transformers/">https://huggingface.co/docs/transformers/</a>
    </p>
    <p>
      [3] <b>Salesforce BLIP Research Documentation</b><br>
      Used for unified vision-language understanding and conditional image captioning.<br>
      Available at: <a href="https://github.com/salesforce/BLIP">https://github.com/salesforce/BLIP</a>
    </p>
    <p>
      [4] <b>PyTorch Documentation</b><br>
      Reference for tensor operations, GPU acceleration, and deep learning model serving.<br>
      Available at: <a href="https://pytorch.org/docs/">https://pytorch.org/docs/</a>
    </p>
    <p>
      [5] <b>Tesseract OCR Engine</b><br>
      Open-source optical character recognition engine sponsored by Google.<br>
      Available at: <a href="https://github.com/tesseract-ocr/tesseract">https://github.com/tesseract-ocr/tesseract</a>
    </p>

    <p style="margin-top: 25px;"><b>AI Tools Used:</b></p>
    <p>
      [1] <b>Google Antigravity & DeepMind Tools</b><br>
      Utilized for architecture optimization, multi-threaded refactoring, and project report formatting.<br>
      Available at: <a href="https://deepmind.google/">https://deepmind.google/</a>
    </p>
  </div>
</div>
""")

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Black Book Project Report - Soham Pandey (TDAI050)</title>
{css}
</head>
<body>
{''.join(pages)}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Generated 50-page HTML at {html_path} ({len(pages)} pages)")

# Compile to PDF using Edge headless
file_url = "file:///" + html_path.replace("\\", "/")
edge_cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    file_url
]

print("Compiling to PDF with Edge headless...")
res = subprocess.run(edge_cmd, capture_output=True, text=True, timeout=60)
if os.path.exists(pdf_path):
    print(f"SUCCESS: Generated {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
else:
    print(f"PDF creation failed: {res.stderr}")
