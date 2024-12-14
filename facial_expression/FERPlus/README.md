cd facial_expression/FERPlus

use WSL or Git Bash
wget https://example.com/path-to-fer-plus-model.pt -O models/fer_plus_weights.pt


use CMD, not PS
conda create -n facial_expression python=3.9 -y
conda activate facial_expression

conda install pytorch torchvision opencv -c pytorch -y
pip install pillow matplotlib

USAGE:
Prepare Input
python scripts/extract_frames.py --input input/video.mp4 --output data/images

Analyze Emotions
python scripts/analyze_emotions.py --input data/images --model models/fer_plus_weights.pt --output data/output/results.csv

Outputs
- Extracted frames: data/images/
- Emotion scores: data/output/results.csv

git clone https://github.com/tomas-gajarsky/facetorch.git
cd facetorch