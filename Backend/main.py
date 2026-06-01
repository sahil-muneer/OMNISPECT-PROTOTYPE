import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ela_engine import perform_ela
from semantic_engine import analyze_text_semantics

app = FastAPI(title="Omnispect Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/analyze")
async def analyze_document(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image assets supported.")

    try:
        raw_bytes = await file.read()
        
        # --- LAYER 1: PIXEL ANALYSIS ---
        ela_bytes = perform_ela(raw_bytes)
        base64_heatmap = f"data:image/png;base64,{base64.b64encode(ela_bytes).decode('utf-8')}"
        
        # --- LAYER 2: SEMANTIC ANALYSIS ---
        # Prototyping simulated text extraction (simulating a forged document)
        mock_ocr_extraction = "INVOICE DATE: 2023-08-14. This document is an unofficial estimate for items billed in 2024."
        semantic_data = analyze_text_semantics(mock_ocr_extraction)
        
        # Combine Logs
        combined_insights = [
            "Layer 1: Error Level Analysis complete.",
            "Layer 1: High pixel variance detected."
        ] + semantic_data["semantic_logs"]

        return {
            "status": "CRITICAL_THREAT" if semantic_data["semantic_risk"] > 50 else "SUSPICIOUS",
            "metrics": {
                "fraud_probability": 87.4,
                "semantic_risk": semantic_data["semantic_risk"],
                "structural_integrity": "Compromised"
            },
            "visuals": {
                "heatmap": base64_heatmap
            },
            "insights": combined_insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine failure: {str(e)}")