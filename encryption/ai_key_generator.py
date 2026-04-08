from encryption.key_manager import generate_key

def evaluate_key_security(sensitivity_score, data_length):
    """
    Decides if a new key should be generated based on AI analysis.
    Returns (should_rotate, reason)
    """
    # High sensitivity threshold (AI score > 0.6)
    if sensitivity_score > 0.6:
        generate_key() # Automatically rotate for high sensitivity
        return True, "High Data Sensitivity Detected (AI Analysis)"
        
    # High length threshold (e.g. > 500 characters)
    if data_length > 500:
        generate_key()
        return True, "Large Data Volume Detected (Enhanced Security)"
        
    # Low sensitivity AND length > 100 
    # (Matches user's example: "less sensitivity and length provide high security")
    if sensitivity_score < 0.4 and data_length > 100:
        generate_key()
        return True, "Adaptive Security Triggered for Extended Content"

    return False, "Normal Security"
