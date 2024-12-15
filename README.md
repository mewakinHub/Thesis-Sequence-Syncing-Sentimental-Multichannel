# **Multi-Channel Sentiment Analysis System** 🎭🎤📝  

This project implements a multi-channel sentiment analysis system that integrates **facial expressions**, **voice tone**, and **speech transcription** to analyze human emotions. A **voting mechanism** is employed to combine results, offering transparency, modularity, and robustness compared to traditional multimodal systems.

---

## **Abstract** 📄  
This system independently analyzes sentiment across three modalities:
- **Facial Expressions** (FERPlus, OpenFace)
- **Voice Tone** (Wav2Vec2 fine-tuned for RAVDESS)
- **Speech Transcriptions** (DistilRoBERTa for emotion detection)

A **post-processing voting mechanism** is applied to combine outputs. Unlike black-box neural networks, this approach is interpretable and adaptable, allowing conflict resolution between emotional signals for a more accurate and explainable sentiment classification.

---

## **System Workflow** 🚀  
The system processes a video file (30-second segments) and performs the following steps:

1. **Frame Extraction**:
   - Convert video into frames at **1-second intervals** for facial expression analysis.  
     📜 Refer: [FacialExpression.md](./docs/FacialExpression.md)  

2. **Speech and Voice Analysis**:
   - Extract audio for **voice tone** and **speech transcription**.  

3. **Modality-Specific Analysis**:
   - **Facial Expression**: Detect frame-level emotions using **Facetorch** or **OpenFace**.
   - **Voice Tone**: Analyze audio tone with **Wav2Vec2**.
   - **Speech Transcription**: Sentiment detection using **DistilRoBERTa**.

4. **Syncing and Voting**:
   - Align outputs across timestamps and apply a weighted **voting mechanism** for final sentiment classification.  
     📜 Refer: [syncing.md](./docs/syncing.md)  

---

## **Voting Mechanism** 🗳️  
The **voting mechanism** assigns dynamic weights to each channel based on their reliability and context:  

| **Modality**            | **Weight** | **Reason**                                                 |
|--------------------------|------------|-----------------------------------------------------------|
| **Speech Transcription** | 0.5        | Clear, context-rich emotional cues.                       |
| **Facial Expression**    | 0.3        | Universally understood cues; reliable for static data.    |
| **Voice Tone**           | 0.2        | Prone to ambiguity; complementary to other channels.      |

**Conflict Resolution**:
- **Positive vs Negative Conflict**: Adjust weights proportionally to conflict ratio.
- **Inter-Chunk Outlier Handling**: Replace short, transient emotion states with "Neutral" for smoother sequences.  
  📜 Refer: [inter-chunk.md](./docs/inter-chunk.md).

---


## **Project Structure** 📂
```
THESIS-SEQUENCE-SYNCING-SYSTEM/
├── docs/                        # Documentation
│   ├── advantage.md             # Advantages of Voting Mechanism
│   ├── CN3-DES400.pdf           # Thesis Report
│   ├── FacialExpression.md      # Facial Expression Model Notes
│   ├── inter-chunk.md           # Inter-Chunk Syncing Details
│   ├── Script-DES400.pdf        # Implementation Notes
│   ├── syncing.md               # Syncing Mechanism Explanation
│   ├── Syncing.pdf              # Syncing Report
│   └── test_dataset.md          # Test Dataset Info
│
├── facial_expression/           # Facial Expression Analysis
│   ├── FERPlus/                 # FERPlus Dataset & Scripts
│   │   ├── data/                # Processed Data
│   │   │   ├── input/           # Raw Input Data
│   │   │   ├── jaffe/           # JAFFE Dataset
│   │   │   ├── jaffe_converted/ # Converted JAFFE Data
│   │   │   ├── labels/          # Emotion Labels
│   │   │   ├── models/          # Trained Models
│   │   │   ├── output/          # Outputs
│   │   │   └── video_frames/    # Extracted Frames
│   │   ├── facetorch/           # Facetorch Source Files
│   │   ├── notebooks/           # Jupyter Notebooks
│   │   ├── scripts/             # Helper Scripts
│   │   │   ├── extract_features.sh
│   │   │   ├── analyze_openface_ferplus.py
│   │   │   └── validate_all.bat
│   │   ├── environment.yml      # Environment Configurations
│   │   ├── README.md            # FERPlus Documentation
│   │   └── .gitattributes       # Git Attributes
│   │
│   └── OpenFace/                # OpenFace Facial Analysis
│       ├── data/                # Input & Output Data
│       │   ├── labels/
│       │   ├── outputs/
│       │   └── results/
│       ├── OpenFace/            # OpenFace Source Files
│       │   ├── build/
│       │   ├── lib/
│       │   ├── imgs/
│       │   ├── packages/
│       │   ├── python_scripts/
│       │   ├── matlab_runners/
│       │   └── model_training/
│       ├── README.md            # OpenFace Notes
│       ├── analyze_openface.py  # OpenFace Execution Script
│       └── extract_features.sh
│
├── input_sample_video/          # Input Videos for Testing
│   ├── negative (angry) - penguinz0/
│   │   ├── sound/               # Extracted Sound Files
│   │   ├── video/               # Video Segments
│   │   └── youtube link.url
│   ├── negative (sad) - logan paul/
│   ├── negative (sad) - markiplier part 1/
│   ├── neutral - mrballen/
│   ├── positive (happy) - tommyinnit/
│   └── positive (sarcastic) - michael reeves/
│
├── voice_tone/                  # Voice Tone Emotion Analysis
│   ├── ...                      # Placeholder for Voice Tone Scripts
│
├── voice_transcription/         # Speech-to-Text Sentiment Analysis
│   ├── ...                      # Placeholder for Transcription Scripts
│
├── .gitignore                   # Git Ignore Configuration
├── output.json                  # Final Output Results
├── README.md                    # Project Documentation
├── requirements.txt             # Python Dependencies
├── syncing.py                   # Syncing Logic Script
└── voting.py                    # Voting Mechanism Script
```

## **Installation** ⚙️  
1. **Clone Repository**:
   ```bash
   git clone https://github.com/your_project_repo.git
   cd your_project_repo
   ```

2. **Setup Environment**:
   ```bash
   conda create -n sentiment_env python=3.9 -y
   conda activate sentiment_env
   pip install -r requirements.txt
   ```

3. **Install Dependencies**:
   - For **Facial Analysis**: Follow instructions in [FERPlus README](./facial_expression/FERPlus/README.md).
   - For **OpenFace**: Refer to [OpenFace Installation](./facial_expression/OpenFace/README.md).

---

## **How to Run** ▶️

1. **Preprocess Video**:
   ```bash
   python scripts/extract_frames.py --input input_sample_video/video.mp4 --output data/frames/
   ```

2. **Run Individual Channels**:
   - Facial Expression Analysis:
     ```bash
     python facial_expression/FERPlus/scripts/analyze_openface.py --input data/frames/ --output data/outputs/facial.json
     ```
   - Voice Tone Analysis:
     ```bash
     python voice_tone/analyze_tone.py --input input_sample_video/video.mp4 --output data/outputs/voice.json
     ```
   - Speech Transcription Analysis:
     ```bash
     python voice_transcription/analyze_transcript.py --input input_sample_video/video.mp4 --output data/outputs/transcript.json
     ```

3. **Combine Results Using Voting**:
   ```bash
   python scripts/voting.py --facial data/outputs/facial.json \
                            --voice data/outputs/voice.json \
                            --transcript data/outputs/transcript.json \
                            --output data/results/final.json
   ```

---

## **Future Work** 🔮  
The method demonstrates improvements over single-channel approaches but has room for enhancements:
1. **Sarcastic Detection**: Analyze **contradictory cues** like happy expressions with angry tone.
2. **Hidden Sadness**: Combine subtle signals (neutral expression, sad voice tone) to detect layered emotions.
3. **Real-Time Processing**: Adapt the system for live-streamed video analysis.

---

## **Results** 📊  
- The system outputs a JSON file with final sentiment classification for each time partition:  
  ```json
  [
      {"partition": "0-6s", "emotion": "Neutral", "confidence": 0.82},
      {"partition": "6-12s", "emotion": "Happy", "confidence": 0.91}
  ]
  ```

- Comparative analysis with single-channel approaches shows improved accuracy, particularly in ambiguous and noisy contexts.  
📜 Full evaluation: [CN3-DES400.pdf](./docs/CN3-DES400.pdf)

---

## **References** 📚  
- Final Report: [CN3-DES400.pdf](./docs/CN3-DES400.pdf)  
- Syncing Logic: [syncing.md](./docs/syncing.md)  
- Facial Expression: [FacialExpression.md](./docs/FacialExpression.md)

---

Let me know if you'd like additional sections or refinements! 🚀