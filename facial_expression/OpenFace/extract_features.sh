#!/bin/bash

# Navigate to OpenFace build directory
cd OpenFace/build

# Run FeatureExtraction for each video
./bin/FeatureExtraction -f "../../../../input_sample_video/positive (sarcastic) - michael reeves/original clip.mp4" -out_dir "../../data/outputs/michael_reeves/"

./bin/FeatureExtraction -f "../../../../input_sample_video/positive (happy) - tommyinnit/original clip.mp4" -out_dir "../../data/outputs/tommyinnit/"

./bin/FeatureExtraction -f "../../../../input_sample_video/neutral - mrballen/original clip.mp4" -out_dir "../../data/outputs/mrballen/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (sad) - markiplier part 1/original clip.mp4" -out_dir "../../data/outputs/markiplier_part1/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (sad) - markiplier part 2/original clip.mp4" -out_dir "../../data/outputs/markiplier_part2/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (sad) - logan paul/original clip.mp4" -out_dir "../../data/outputs/logan_paul/"

./bin/FeatureExtraction -f "../../../../input_sample_video/negative (angry) - penguinz0/original clip.mp4" -out_dir "../../data/outputs/penguinz0/"

echo "Feature extraction completed for all videos."
