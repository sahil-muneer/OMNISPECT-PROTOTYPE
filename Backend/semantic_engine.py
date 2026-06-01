import re

def analyze_text_semantics(extracted_text: str):
    """
    Layer 2: Scans document text for logical inconsistencies, 
    mismatched timelines, and unauthorized keywords.
    """
    insights = []
    risk_score = 0
    
    # Rule 1: High-Risk Keyword Detection
    suspicious_keywords = ['estimate', 'draft', 'unofficial', 'void', 'sample', 'amended']
    found_words = [word for word in suspicious_keywords if word in extracted_text.lower()]
    
    if found_words:
        insights.append(f"Layer 2 Alert: Unauthorized document type indicators found -> {', '.join(found_words)}")
        risk_score += 45
        
    # Rule 2: Temporal Anomalies (Looking for forged/mismatched dates)
    # Extracts all years starting with 20xx
    years_found = re.findall(r'\b(20[0-2][0-9])\b', extracted_text)
    unique_years = set(years_found)
    
    if len(unique_years) > 1:
        insights.append(f"Layer 2 Alert: Conflicting timeline detected. Multiple years found: {', '.join(unique_years)}")
        risk_score += 35

    if risk_score == 0:
        insights.append("Layer 2: Semantic cross-validation passed. Text timeline is consistent.")

    return {
        "semantic_risk": min(risk_score, 100),
        "semantic_logs": insights
    }