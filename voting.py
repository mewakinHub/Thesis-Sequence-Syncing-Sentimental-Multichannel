import os
import json
from collections import defaultdict

# Define weights for each modality
WEIGHTS = {
    "transcript": 0.5,
    "facial_expression": 0.3,
    "voice_tone": 0.2
}

# Define emotion categories
NEGATIVE_EMOTIONS = {"Angry", "Disgust", "Fear", "Sad"}
POSITIVE_EMOTIONS = {"Happy", "Surprise"}

# Function to calculate conflict weight adjustment
def adjust_weight_for_conflict(emotions):
    positive_count = sum(1 for e in emotions if e["emotion"] in POSITIVE_EMOTIONS)
    negative_count = sum(1 for e in emotions if e["emotion"] in NEGATIVE_EMOTIONS)

    if positive_count > 0 and negative_count > 0:  # Conflict exists
        total_count = positive_count + negative_count
        conflict_ratio = min(positive_count, negative_count) / total_count
        return 1 - conflict_ratio  # Reduce weight based on conflict ratio

    return 1  # No conflict, full weight

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
        facial_expressions = partition_data["facial_expression"]
        adjusted_weight = WEIGHTS["facial_expression"] * adjust_weight_for_conflict(facial_expressions)
        for expression in facial_expressions:
            emotion_scores[expression["emotion"]] += expression["confidence"] * adjusted_weight
        total_weight += adjusted_weight

    # Voice tone contribution
    if "voice_tone" in partition_data:
        voice_tones = partition_data["voice_tone"]
        adjusted_weight = WEIGHTS["voice_tone"] * adjust_weight_for_conflict(voice_tones)
        for tone in voice_tones:
            emotion_scores[tone["emotion"]] += tone["confidence"] * adjusted_weight
        total_weight += adjusted_weight

    # Normalize scores by total weight
    for emotion in emotion_scores:
        emotion_scores[emotion] /= total_weight

    # Find the emotion with the highest score
    final_emotion = max(emotion_scores, key=emotion_scores.get)
    return final_emotion, emotion_scores[final_emotion]

def refine_emotion_transitions(partition_results, stability_threshold=2):
    refined_results = []
    current_emotion = None
    current_streak = []

    for result in partition_results:
        partition_emotion = result["final_emotion"]

        if partition_emotion == "Neutral":
            # Finalize current streak
            if current_streak:
                # Check if the streak is too short
                refined_results.extend(current_streak)
                current_streak = []
            # Append Neutral as is
            refined_results.append(result)
            continue

        # Handle valid emotions
        if partition_emotion == current_emotion:
            current_streak.append(result)
        else:
            # Finalize current streak if it exists
            if current_streak:
                if len(current_streak) < stability_threshold:
                    for streak_result in current_streak:
                        streak_result["final_emotion"] = "Neutral"
                refined_results.extend(current_streak)

            # Start a new streak
            current_emotion = partition_emotion
            current_streak = [result]

    # Finalize the last streak
    if current_streak:
        if len(current_streak) < stability_threshold:
            for streak_result in current_streak:
                streak_result["final_emotion"] = "Neutral"
        refined_results.extend(current_streak)

    return refined_results

# Ensure the output directory exists
output_dir = "Final_voting"
os.makedirs(output_dir, exist_ok=True)

# Read the output.json file
with open("output.json", "r") as f:
    data = json.load(f)

# Process each partition
raw_results = []
for partition in data:
    final_emotion, confidence = calculate_weighted_emotion(partition)
    raw_results.append({
        "partition": partition["partition"],
        "final_emotion": final_emotion,
        "confidence": confidence
    })

# Refine results to filter noise
refined_results = refine_emotion_transitions(raw_results)

# Save refined results to a file
output_file = os.path.join(output_dir, "refined_results.json")
with open(output_file, "w") as f:
    json.dump(refined_results, f, indent=4)

# Output refined results
for result in refined_results:
    print(f"Partition: {result['partition']}, Final Emotion: {result['final_emotion']}, Confidence: {result['confidence']:.2f}")
