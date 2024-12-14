import json
from pydub import AudioSegment
from pydub.utils import make_chunks
import whisper
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def split_audio(file_path, chunk_length_ms=30000):
    audio = AudioSegment.from_file(file_path)
    chunks = make_chunks(audio, chunk_length_ms)
    return chunks

def transcribe_audio(chunks):
    model = whisper.load_model("base")
    results = []
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk_{i}.wav", format="wav")
        result = model.transcribe(f"chunk_{i}.wav")
        for segment in result["segments"]:
            results.append({
                "time": segment["end"],
                "transcript": segment["text"],
                "confidence": segment["avg_logprob"]
            })
    return results

def analyze_emotions(transcripts):
    emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    emotion_results = []
    for item in transcripts:
        emotion = emotion_analyzer(item["transcript"])[0]
        emotion_results.append({
            "time": item["time"],
            "emotion": emotion["label"].lower(),
            "confidence": emotion["score"],
            "transcript": item["transcript"]
        })
    return emotion_results

if __name__ == "__main__":
    file_path = "sounds/neutral (calm) - mrballen - sound.wav"
    chunks = split_audio(file_path, chunk_length_ms=30000)
    transcription_results = transcribe_audio(chunks)
    emotion_results = analyze_emotions(transcription_results)

    output_file = "output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(emotion_results, f, indent=4, ensure_ascii=False)

    print(f"Emotion results written to {output_file}")
