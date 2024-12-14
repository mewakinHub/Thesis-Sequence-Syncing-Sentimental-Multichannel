# Face Verification Project

This is a simple project using the `DeepFace` library to verify if two images are of the same person.

## Prerequisites

- Python 3.6+
- Install the required libraries

```bash
pip install deepface opencv-python
pip install tf-keras
pip install tensorflow==2.10.0
```

## Project Structure

```
face_verification_project/
├── images/
│   ├── img1.jpg          # First image for verification
│   ├── img2.jpg          # Second image for verification
├── verify_face.py        # Main script
└── README.md             # Instructions
```

## Usage

1. Place two images you want to compare in the `images/` directory and name them `img1.jpg` and `img2.jpg`.
   
2. Run the script:

```bash
python verify_face.py
```

## Output

The script will print whether the two images contain the same person and a confidence score.
```

### Running the Project

1. Place your images in the `images/` folder and name them `img1.jpg` and `img2.jpg`.
2. Run the following command to execute the script:

   ```bash
   python verify_face.py
   ```

This minimal setup provides a simple face verification utility using `DeepFace`. The README guides through installation, setup, and running the code. Let me know if you need further customization!