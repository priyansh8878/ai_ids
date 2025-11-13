import random

# Mock prediction function
def predict_intrusion(features):
    """
    Simulate an AI model prediction.
    Input: features = [duration, packet_size, 500, protocol_number]
    Output: 'Intrusion' or 'Normal'
    """
    # Simple heuristic: if packet_size > 1000 or duration > 500 ms, flag as intrusion
    duration, packet_size, _, protocol_val = features
    if packet_size > 1000 or duration > 500:
        return "Intrusion"
    # Random small chance to simulate AI uncertainty
    if random.random() < 0.1:
        return "Intrusion"
    return "Normal"

# Mock explanation function (can later integrate OpenAI GPT)
def explain_intrusion(event_data, prediction):
    """
    Provide a textual explanation for the AI prediction.
    """
    if prediction == "Intrusion":
        reason = []
        if event_data['packet_size'] > 1000:
            reason.append(f"large packet size ({event_data['packet_size']})")
        if int(event_data.get('duration', 0)) > 500:
            reason.append(f"long duration ({event_data['duration']} ms)")
        reason_text = " and ".join(reason) if reason else "suspicious activity detected"
        return f"Predicted Intrusion due to {reason_text}."
    else:
        return "Network traffic appears normal."
