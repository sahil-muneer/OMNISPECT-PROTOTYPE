# 🛡️ OMNISPECT // Real-Time Threat Analysis Gateway

**A dual-layer digital forensics pipeline built to detect forgery and tampering across land records, legal documents, and financial statements.**

Omnispect was engineered to solve a critical vulnerability in modern banking and underwriting: the rise of high-quality document forgery. Standard visual checks by human underwriters are no longer sufficient. Omnispect provides a multi-modal, automated threat analysis gateway that integrates directly into enterprise workflows.

---

## 🚀 Key Features

* **Layer 1: Error Level Analysis (ELA) Engine**
  Utilizes OpenCV to calculate pixel compression variance. By compressing and decompressing the image matrix, it generates a high-contrast heatmap that exposes structural tampering, cloning, and digital splicing invisible to the human eye.
* **Layer 2: Semantic Cross-Validation Engine**
  A Python-based rules engine that parses document text to detect logical traps. It flags temporal anomalies (e.g., mismatched years across a single document) and unauthorized keywords (e.g., "estimate", "void", "sample") to catch sophisticated forgeries that bypass visual checks.
* **Cryptographic Audit Trails**
  Generates a SHA-256 digital fingerprint for every uploaded asset, ensuring strict legal compliance and proving the exact document analyzed was not altered post-upload.
* **Enterprise PDF Reporting**
  Generates native, downloadable forensic reports directly from the dashboard for seamless integration into underwriting audit logs.

---

## 💻 Tech Stack

* **Frontend:** React, Vite, Tailwind CSS
* **Backend:** FastAPI, Python
* **Computer Vision:** OpenCV, NumPy
* **Data Parsing:** Python Regex (re)

---

## 🛠️ How to Run Locally

### 1. Start the Backend (FastAPI)
```bash
cd backend
# Activate virtual environment (Windows)
.\venv\Scripts\activate
# Install dependencies
pip install fastapi uvicorn python-multipart opencv-python numpy
# Boot the server
uvicorn main:app --reload --port 8000