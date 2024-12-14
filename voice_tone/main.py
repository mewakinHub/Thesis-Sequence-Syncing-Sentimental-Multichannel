import json
from pydub import AudioSegment
from pydub.utils import make_chunks
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def split_audio(file_path, chunk_length_ms=5000):
    audio = AudioSegment.from_file(file_path)
    chunks = make_chunks(audio, chunk_length_ms)
    return chunks

def analyze_voice_tone(chunks):
    emotion_analyzer = pipeline("audio-classification", model="Dpngtm/wav2vec2-emotion-recognition")
    emotion_results = []
    for i, chunk in enumerate(chunks):
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        emotion = emotion_analyzer(chunk_path)[0]
        emotion_label = emotion["label"].lower()
        if emotion_label == "label_0":
            emotion_label = "Angry"
        elif emotion_label == "label_1":
            emotion_label = "Neutral"
        elif emotion_label == "label_2":
            emotion_label = "Disgust"
        elif emotion_label == "label_3":
            emotion_label = "Fear"
        elif emotion_label == "label_4":
            emotion_label = "Happy"
        elif emotion_label == "label_5":
            emotion_label = "Neutral"
        elif emotion_label == "label_6":
            emotion_label = "Sad"
        elif emotion_label == "label_7":
            emotion_label = "Surprise"
        else:
            emotion_label = "Neutral"
        emotion_results.append({
            "time": (i + 1) * 5,
            "emotion": emotion_label,
            "confidence": emotion["score"]
        })
    return emotion_results

if __name__ == "__main__":
    file_name = "positive (sarcastic) - michael reeves - sound"
    file_path = f"sounds/{file_name}.wav"
    chunks = split_audio(file_path, chunk_length_ms=5000)
    emotion_results = analyze_voice_tone(chunks)
    output_file = "output_tone.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(emotion_results, f, indent=4, ensure_ascii=False)
    print(f"Voice tone analysis results written to {output_file}")
