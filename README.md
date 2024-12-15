# **Multi-Channel Sentiment Analysis with Voting Mechanism** 🎭🎤📝  
This repository provides an implementation of a **multi-channel sentiment analysis** system that uses **facial expression**, **voice tone**, and **speech transcription** to classify human emotions. By employing a **voting mechanism** instead of traditional multimodal fusion, the system ensures flexibility, transparency, and adaptability to dynamic scenarios.

---

## **Purpose** 📚
Traditional **single-channel sentiment analysis** and **early fusion multimodal systems** face challenges in handling:
1. Noise in real-world data.
2. Conflicts between emotional signals.
3. Lack of interpretability (e.g., black-box neural networks).

This project introduces a **post-processing voting mechanism** that:
- Combines independent outputs from multiple channels.
- Resolves conflicts with dynamic thresholds and conditions.
- Enhances interpretability and modularity.

🔗 **Detailed Explanation**:  
- [Advantages of Voting Mechanism](./docs/advantage.md)  
- [Facial Expression Analysis](./docs/FacialExpression.md)  
- [Syncing Mechanism](./docs/syncing.md)  

---

## **Features** 🚀
1. **Facial Expression Analysis**:
   - Use models like **Facetorch (FER-like)** and **OpenFace** for static and dynamic frame analysis.
   - Outputs per-frame emotions with timestamps.  
   ➡️ [FacialExpression.md](./docs/FacialExpression.md)

2. **Voice Tone Analysis**:
   - Utilize **Wav2Vec2** models for speech emotion recognition.
   - Detects vocal emotions such as **Happy, Sad, Angry, Calm, Neutral**.  

3. **Speech Transcription Sentiment**:
   - Transcribe speech using **Google Speech-to-Text** or **Whisper**.
   - Analyze sentiment using **DistilRoBERTa** for **positive, negative, and neutral** classifications.

4. **Voting Mechanism**:
   - Combines results from all channels after independent analysis.
   - Dynamically resolves conflicts and handles edge cases.  
   ➡️ [Syncing.md](./docs/syncing.md)

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

---

## **Installation** ⚙️

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_project_repo.git
   cd your_project_repo
   ```

2. **Set Up Environment**:
   ```bash
   conda create -n sentiment_env python=3.9 -y
   conda activate sentiment_env
   pip install -r requirements.txt
   ```

3. **Install OpenFace and Facetorch**:
   Follow the guides in [FacialExpression.md](./docs/FacialExpression.md).

---

## **How to Run** ▶️

1. **Extract Frames for Facial Analysis**:
   ```bash
   python scripts/extract_frames.py --input ./input_sample_video/video.mp4 --output ./data/frames/
   ```

2. **Run Facial, Voice, and Text Analysis**:
   - **Facial Expression**:
     ```bash
     python scripts/analyze_openface.py --input ./data/frames/ --output ./data/outputs/facial_results.json
     ```
   - **Voice Tone**:
     ```bash
     python voice_tone/analyze_tone.py --input ./input_sample_video/video.mp4 --output ./data/outputs/voice_results.json
     ```
   - **Speech Transcription**:
     ```bash
     python voice_transcription/analyze_transcript.py --input ./input_sample_video/video.mp4 --output ./data/outputs/transcript_results.json
     ```

3. **Run the Voting Mechanism**:
   ```bash
   python scripts/voting.py --facial ./data/outputs/facial_results.json \
                            --voice ./data/outputs/voice_results.json \
                            --transcript ./data/outputs/transcript_results.json \
                            --output ./data/results/final_sentiment.json
   ```

4. **Review Results**:
   The final sentiment results will be saved in `./data/results/final_sentiment.json`.

---

## **Results** 📊

Sample Output:
```json
[
    {
        "partition": "0-6s",
        "final_emotion": "Neutral",
        "confidence": 0.85
    },
    {
        "partition": "6-12s",
        "final_emotion": "Happy",
        "confidence": 0.92
    },
    {
        "partition": "12-18s",
        "final_emotion": "Conflicted",
        "confidence": 0.45
    }
]
```

---

## **Advantages** 🏆  
1. **Flexibility**: Easily replace or update models for each channel.  
2. **Noise Tolerance**: Filters inconsistent results using thresholds and stability conditions.  
3. **Modular Design**: Each channel operates independently, improving scalability.  
4. **Transparency**: Enhances interpretability compared to black-box neural networks.

➡️ **More Details**: [Advantages of Voting](./docs/advantage.md)

---

## **Future Work** 🔮
- **Real-Time Processing**: Extend for live video inputs.  
- **Advanced Conflict Resolution**: Handle sarcastic and mixed emotions.  
- **Improved Accuracy**: Fine-tune models with real-world emotional datasets.

---

## **Contributing** 🤝
Feel free to fork, raise issues, or contribute to this project.  
Refer to the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## **References** 📚
1. **Thesis Report**: [Full Report](./docs/CN3-DES400.pdf)  
2. **Facial Analysis**: [FacialExpression.md](./docs/FacialExpression.md)  
3. **Syncing Logic**: [Syncing.md](./docs/syncing.md)

---

## **License** 📄
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

