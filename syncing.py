import json
from collections import defaultdict

# Load data from the files
file1_path = "facial_expression/FERPlus/data/output/logan_paul_validation.txt"
file2_path = "voice_tone/output_tone_logan_paul.json"
file3_path = "voice_transcription/output_transcription_logan_paul.json"

# Read the first file (facial expressions)
with open(file1_path, "r") as f:
    facial_data_lines = f.readlines()[2:]  # Skip header lines
facial_data = []
for line in facial_data_lines:
    parts = line.strip().split(", ")
    facial_data.append({
        "frame": parts[0].replace("frame_", ""),
        "emotion": parts[2],
        "confidence": float(parts[3])
    })

# Read the second file (voice tones)
with open(file2_path, "r") as f:
    voice_data = json.load(f)

# Read the third file (transcripts)
with open(file3_path, "r") as f:
    transcript_data = json.load(f)

# Generate partitions based on the third file (transcripts)
result = []
previous_end_time = 0.0  # Start from 0.0 for the first partition

for i, entry in enumerate(transcript_data):
    start_time = previous_end_time  # Start where the previous partition ended
    end_time = entry["time"]  # End time is the current entry's time

    partition = {
        "partition": f"{int(start_time)}-{int(end_time)}s",
        "transcript": {
            "text": entry["transcript"],
            "emotion": entry["emotion"],
            "confidence": entry["confidence"]
        },
        "facial_expression": [],
        "voice_tone": []
    }

    # Add facial expressions that fall into this partition
    for facial_entry in facial_data:
        frame_time = int(facial_entry["frame"].replace("frame_", "").replace(".jpg", ""))
        if start_time <= frame_time < end_time:
            partition["facial_expression"].append({
                "frame": facial_entry["frame"],  # Keep the full filename
                "emotion": facial_entry["emotion"],
                "confidence": facial_entry["confidence"]
            })

    # Add voice tones that fall into this partition
    for voice_entry in voice_data:
        if start_time <= voice_entry["time"] < end_time:
            partition["voice_tone"].append(voice_entry)

    # Save this partition and update the previous end time
    result.append(partition)
    previous_end_time = end_time

# Save the resulting structure
output_path = "output.json"
with open(output_path, "w") as f:
    json.dump(result, f, indent=4)

print(f"Synced data saved to {output_path}")