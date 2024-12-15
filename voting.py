import json
from collections import defaultdict

# Define weights for each modality
WEIGHTS = {
    "transcript": 0.5,
    "facial_expression": 0.3,
    "voice_tone": 0.2
}

# Function to calculate weighted emotions
def calculate_weighted_emotion(partition_data):
    emotion_scores = defaultdict(float)
    total_weight = 0

    # Transcript contribution
    if "transcript" in partition_data:
        transcript = partition_data["transcript"]
        emotion_scores[transcript["emotion"]] += transcript["confidence"] * WEIGHTS["transcript"]
        total_weight += WEIGHTS["transcript"]

    # Facial expression contribution
    if "facial_expression" in partition_data:
        for expression in partition_data["facial_expression"]:
            emotion_scores[expression["emotion"]] += expression["confidence"] * WEIGHTS["facial_expression"]
        total_weight += WEIGHTS["facial_expression"]

    # Voice tone contribution
    if "voice_tone" in partition_data:
        for tone in partition_data["voice_tone"]:
            emotion_scores[tone["emotion"]] += tone["confidence"] * WEIGHTS["voice_tone"]
        total_weight += WEIGHTS["voice_tone"]

    # Normalize scores by total weight
    for emotion in emotion_scores:
        emotion_scores[emotion] /= total_weight

    # Find the emotion with the highest score
    final_emotion = max(emotion_scores, key=emotion_scores.get)
    return final_emotion, emotion_scores[final_emotion]

# Read the output.json file
with open("output.json", "r") as f:
    data = json.load(f)

# Process each partition
results = []
for partition in data:
    final_emotion, confidence = calculate_weighted_emotion(partition)
    results.append({
        "partition": partition["partition"],
        "final_emotion": final_emotion,
        "confidence": confidence
    })

# Output results
for result in results:
    print(f"Partition: {result['partition']}, Final Emotion: {result['final_emotion']}, Confidence: {result['confidence']:.2f}")
