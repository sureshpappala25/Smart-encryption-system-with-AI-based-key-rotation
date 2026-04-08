import pandas as pd
import numpy as np
import os
from encryption.sensitivity_analyzer import analyze_sensitivity

# Paths to datasets
USER_LOGS_PATH = 'dataset/user_access_logs.csv'
THREAT_PATTERNS_PATH = 'dataset/threat_patterns.csv'

def analyze_behavior(user_id):
    """
    Analyzes user behavior logs to detect anomalies.
    Returns a score between 0.0 and 1.0.
    """
    if not os.path.exists(USER_LOGS_PATH):
        return 0.2
    
    try:
        df = pd.read_csv(USER_LOGS_PATH)
        user_data = df[df['user_id'] == user_id]
        
        if user_data.empty:
            return 0.2 # Baseline risk for new users
            
        avg_access = df['access_count'].mean()
        user_access = user_data['access_count'].iloc[0]
        
        # Normalizing risk: if access is 2x the average, risk is high.
        risk = min(1.0, user_access / (avg_access * 2))
        return float(risk)
    except Exception:
        return 0.3

def detect_threat(pattern_name):
    """
    Checks if a network traffic pattern or activity matches known threat signatures.
    """
    if not os.path.exists(THREAT_PATTERNS_PATH):
        return 0.1
        
    try:
        df = pd.read_csv(THREAT_PATTERNS_PATH)
        match = df[df['pattern'] == pattern_name.lower()]
        
        if match.empty:
            # Check for partial matches or return safe score
            if 'normal' in pattern_name.lower():
                return 0.1
            return 0.4 # Unknown pattern
            
        return float(match['score'].iloc[0])
    except Exception:
        return 0.5

def get_risk_assessment(user_id, pattern, data_text):
    """
    Comprehensive AI Analysis Engine:
    Combines behavior, traffic threats, and data sensitivity.
    """
    behavior_score = analyze_behavior(user_id)
    threat_score = detect_threat(pattern)
    sensitivity_score = analyze_sensitivity(data_text)
    
    # Weighted calculation for unified risk assessment
    # 40% Threat Pattern, 30% User Behavior, 30% Data Sensitivity
    unified_risk = (threat_score * 0.4) + (behavior_score * 0.3) + (sensitivity_score * 0.3)
    
    return {
        "unified_risk": round(unified_risk, 2),
        "behavior_score": round(behavior_score, 2),
        "threat_score": round(threat_score, 2),
        "sensitivity_score": round(sensitivity_score, 2),
        "recommendation": "Rotate Key" if unified_risk > 0.6 else "Secure"
    }
