for Facial Expression channel, we might use the Deep Face model

do the frame by frame model detection on fix sampling rate, then label the result with the Key attribute as Time for determining how to sync with other channels

Model Resource: hugging face, or etc.

Model Form: api, library, .pt, etc.

Github code: [facial_expression folder](/facial_expression/)

### PURPOSE: Switching Multiple Models to demonstrate the flexibility & modularity advantage of the voting mechanism approach, than the traditional multi-modal

    #### KEY FOCUS: Benefits of able to switching Multiple Models:
    1. **Proving seamless Adaptability**:
    - Implementing two or more models (e.g., DeepFace and another specialized model) shows that your system can seamlessly switch or combine outputs, highlighting the flexibility of your post-processing mechanism over multimodal systems.
    2. **Handling Diverse Scenarios**: -> use metric like accuracy from validating with real answer for comparison
    - Different models may excel in specific situations (e.g., one might perform better in static images while another in dynamic video). Combining outputs can enhance reliability.

    #### Implementation Strategy:
    - Start with **DeepFace** as a *baseline* for facial expression analysis.
    - Research and test at least one alternative model, such as:
        1. **AffectNet or FER+**: Models tailored for emotion recognition.
        2. **OpenFace**: Highly interpretable and robust for academic research.
        - **Custom Model**: Train a CNN or transformer-based architecture if time and resources allow.

    #### TODO:
    1. finish 2 models
        - fix sampling rate
        - use time for time stamp labelling from the video length

    2. post processing by converting the result form into JSON form contained dictionary of {timestamp, accuracy, emotion, sentiment}

    3. Syncing with other channel based on timestamp matching
        - if-else condition strategy for contrast accuracy or emotion from the on-going consecutive sequenced results by using dynamic threshold or state to prevent noise or false detection
            - use Post-Processing JSON as input, but change the form of each time stamp in the middle of processing!



### Model Selection:
- what is the strategy and method to select the model?
- objective of these model?

---

###### **Key Behaviors** - Neither is “Always Better”
| **Aspect**               | **Facetorch (FER-like)**         | **OpenFace**                        |
|--------------------------|----------------------------------|-------------------------------------|
| **Based On**             | FER2013/FER+ dataset            | Dynamic facial analysis techniques |
| **Emotion Analysis**     | Single image/frame-based        | Video-based, with temporal context |
| **Good For**             | Quick Static emotion detection  | Dynamic expressions over time      |
| **Handles Videos Well?** | No (frame-by-frame, prone to errors) | Yes (tracks facial dynamics)       |
| **Customization**        | Use models trained on FER datasets | Action Units, temporal tracking    |
| **Weakness**	           | Can’t see changes over time	 | Requires more data and processing  |

###### **When to Use What?**
1. **Facetorch**:
   - Best for **single images** or exploratory tasks where analyzing static expressions is enough.
   - Use if you're limited on time and need a quick solution.
   - Example: Processing a dataset of selfies or passport photos.

2. **OpenFace**:
   - Best for **video analysis** where you need to track changes in facial expressions over time.
   - Use if your project involves:
     - Videos with facial expression transitions.
     - Groups of people interacting or subtle micro-expressions.
   - Example: Analyzing emotional reactions during a conversation or in a movie scene.

---

#### 0. Deep Face - general purpose(not sentiment specialize) -- might not use anymore
The DeepFace library uses multiple backend models, such as VGG-Face, OpenFace, Google FaceNet, and others.

    #### Pros of Using DeepFace:
    1. **Established Benchmark**: DeepFace is a widely recognized model with a proven track record in facial recognition and expression analysis.
    2. **Ease of Integration**: It is *pre-trained* and easy to integrate into systems, saving development time.
    3. **Baseline Performance**: Provides a strong baseline for facial expression analysis that can serve as a starting point to benchmark other models.

    #### Why Consider Alternatives?
    1. **Specialization for Emotion Analysis**:
    - DeepFace is more *tuned for facial recognition and identity matching rather than sentiment or emotion analysis*. There may be better models, such as FER+ or models built specifically for emotion recognition.
    2. **Flexibility in Features**:
    - Some newer models offer better handling of subtle facial expressions, micro-expressions, or dynamic analysis across video frames.
    3. **Edge Case Handling**:
    - If the dataset contains nuanced or complex emotional states, exploring models like OpenFace, Affectiva, or even custom-trained neural networks on a tailored dataset may yield better results.

#### 1. Facetorch - "FER-like" (Single Image Capability)
- Facetorch is a Python library designed for face analysis, integrating open-source community models.
- Uses **pre-trained models**, trained on various FER datasets, but not explicit mention of FER+ and FER2013 in Facetorch documentation.
- Specifically designed for emotion recognition, so identify subtle emotional nuances like contempt, which general-purpose models like DeepFace might miss.

RESOURCE:
paperwithcode of FER dataset: https://paperswithcode.com/task/facial-expression-recognition?page=3
Facetorch github: https://github.com/tomas-gajarsky/facetorch
Facetorch demo app: https://huggingface.co/spaces/tomas-gajarsky/facetorch-app

#### **Facetorch vs. FER+ vs. OpenFace**
- **FER (Facial Expression Recognition)** is a **dataset**, specifically:
  - **FER2013**: A widely used dataset with 35,000 grayscale images of faces labeled into 7 basic emotions (Happy, Sad, Angry, Surprise, Neutral, Disgust, Fear).
  - **FER+**: An improved version of FER2013 with better annotations (e.g., multiple annotators, refined emotion classes).
- **FER Models**:
  - Models like Facetorch and others are **trained on the FER dataset** (FER2013 or FER+). These are **pre-trained models**, not the datasets themselves.
  - Example: FER+ isn’t a model; it’s a dataset. A "FER+ model" would refer to a model trained on the FER+ dataset.

##### static frame-by-frame input: "snapshot emotion detector."
INPUT Example: If you have a profile picture or a moment in a video where someone smiles, it can recognize emotions like happiness, sadness, anger, etc.

PROS:
- Designed for **single-image emotion detection**. It works well when processing individual images or static frames
CONS:
- It does not consider temporal information (movement across frames, it doesn’t account for expression changes over time in videos), focusing on static image analysis.
- Most implementations expect images as input. You'll need to preprocess .mp4 into frames.
- Is prone to misclassifications in video frames due to motion blur, low-quality frames, or subtle expressions.


#### 2. Use OpenFace
INPUT Example: If you have a profile picture or a moment in a video where someone smiles, it can recognize emotions like happiness, sadness, anger, etc.

OpenFace is specialized for analyzing facial dynamics, so it works best with videos directly.
better with movement detection from consecutive frame
  - Designed specifically for **video-based facial analysis** and **dynamic expressions**.
  - Tracks **facial landmarks and dynamics over time**. This makes it much better for capturing the evolution of expressions in videos.
  - Outputs include:
    - Action Units (AUs): Muscle movements that correlate with emotions.
    - Temporal features (e.g., how expressions change across frames).
  - More suitable for scenarios where facial expressions change over time or when dealing with group interactions.

##### temporal context from consecutive frame expression changing: dynamic emotion detector

PROS:
- Accepts .mp4 directly and considers facial dynamics over time (e.g., how a smile develops or a frown deepens).
- Extracts temporal features automatically from video.
- Use OpenFace for dynamic temporal analysis to show a richer understanding of facial expressions.
- don’t need to manually divide expressions into separate segments before inputting the video. OpenFace is designed to handle and analyze continuous sequences of facial expressions and will track the changes automatically over time.
    1. **Designed for Dynamic Analysis**:
    - OpenFace excels at analyzing facial expressions frame-by-frame over time. It tracks Action Units (AUs), gaze, and head movements, which are inherently dynamic.
    - If your video includes transitions between expressions (e.g., angry → neutral → angry), OpenFace will pick up these changes.

    2. **Temporal Context**:
    - OpenFace uses temporal data to understand the transitions and patterns, so dividing the video into separate expressions might actually reduce its effectiveness.
    - For example, it can identify that someone transitioned from an angry face to a neutral face, providing richer insights than if you analyzed each part in isolation.

    3. **Automated Output**:
    - OpenFace generates outputs like AU intensities, probabilities of facial expressions, or time-series data of detected emotions. This means it inherently recognizes and logs the changes in expressions over time.
    
    **Why Not Divide Beforehand?**
    - Dividing the video before inference can lead to a loss of temporal context (e.g., OpenFace won’t know that the angry expression followed a neutral one).
    - It increases manual work unnecessarily, as OpenFace is already capable of detecting and distinguishing multiple expressions over time.
CONS:

confusing topic:
1. OpenFace produces Action Units (AUs) and other data (like head pose, eye gaze), which can be parsed to infer emotions.

### 2 inputs for comparison
1. single image snapshot samples for showing how FER+ get better result than OpenFace
2. video for show that OpenFace better than FER+ on consecutive frame-by-frame captured detection

---

### How to Set-up & Run

#### 0. Deep Face - general purpose(not sentiment specialize)

#### 1. AffectNet (FER+)
conda create -n facial_expression python=3.9 -y
conda activate facial_expression

git clone https://github.com/tomas-gajarsky/facetorch.git
# Download EfficientNet-B0 Model
gdown --id 1i5f8vy1dZv_u8vsJsj9CHEzHwsokIknr -O data\models\1\model.pt

# Download EfficientNet-B2 Model
gdown --id 1xoB5VYOd0XLjb-rQqqHWCkQvma4NytEd -O data\models\2\model.pt


DETAIL: [../facial_expression/FERPlus/](../facial_expression/FERPlus/README.md)
- multiple individual image folder
- consecutive frame of video

#### 2. OpenFace
For OpenFace, you **don’t need to manually divide expressions into separate segments** before inputting the video. OpenFace is designed to handle and analyze continuous sequences of facial expressions and will track the changes automatically over time. Here’s why and how it works:

### **How to Handle Videos with Many Expressions:**

1. **Input the Whole Video**:
   - Provide the full 15-second clip to OpenFace. Ensure the face is visible and well-lit throughout the clip for optimal analysis.

2. **Analyze the Timeline**:
   - OpenFace will generate time-stamped data showing how facial expressions evolve over the video. For example:
     - At second 1–5: Angry face (AU4, AU7 activated).
     - At second 6–10: Neutral face (minimal AU activation).
     - At second 11–15: Angry face again (AU4, AU7 reactivated).

3. **Visualize the Data**:
   - Use visualization tools (like plotting AU intensities or probabilities over time) to make sense of the emotional dynamics. This will let you see the expression changes clearly without manually segmenting the video.

---

### **Workflow for Your Case:**
1. Input the full 15-second video into OpenFace.
2. Let it analyze the entire timeline of facial dynamics.
3. Examine the output for:
   - Time-series data showing AU activations.
   - Probabilities of specific emotions over time.
   - Changes in facial movements across frames.
4. If needed, segment or summarize the data after inference to focus on specific periods or transitions.


------
