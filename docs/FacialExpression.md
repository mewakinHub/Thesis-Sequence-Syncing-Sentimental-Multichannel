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

#### 0. Deep Face - general purpose(not sentiment specialize)
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

#### 1. AffectNet (FER+)
specialize on sentimental than Deepface
- Specifically designed for emotion recognition.
- Can identify subtle emotional nuances like contempt, which general-purpose models like DeepFace might miss.

##### static frame-by-frame input: advantage & disadvantage

PROS:
CONS:
- It does not consider temporal information (movement across frames), focusing on static image analysis.
- Most implementations expect images as input. You'll need to preprocess .mp4 into frames.


#### 2. Use OpenFace
OpenFace is specialized for analyzing facial dynamics, so it works best with videos directly.
better with movement detection form consecutive frame

##### static frame-by-frame input: advantage & disadvantage

PROS:
- Accepts .mp4 directly and considers facial dynamics over time (e.g., how a smile develops or a frown deepens).
- Extracts temporal features automatically from video.
- Use OpenFace for dynamic temporal analysis to show a richer understanding of facial expressions.
CONS:

confusing topic:
1. OpenFace produces Action Units (AUs) and other data (like head pose, eye gaze), which can be parsed to infer emotions.

---

### How to Set-up

#### 0. Deep Face - general purpose(not sentiment specialize)

#### 1. AffectNet (FER+)


#### 2. Use OpenFace

