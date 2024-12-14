@echo off

echo model v1
python scripts\analyze_emotions_with_validation.py --input data\video_frames\penguinz0 --output data\output\penguinz0_validation.txt --model data\models\1\model.pt --labels data\labels\penguinz0.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\michael_reeves --output data\output\michael_reeves_validation.txt --model data\models\1\model.pt --labels data\labels\michael_reeves.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\tommyinnit --output data\output\tommyinnit_validation.txt --model data\models\1\model.pt --labels data\labels\tommyinnit.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\mrballen --output data\output\mrballen_validation.txt --model data\models\1\model.pt --labels data\labels\mrballen.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\markiplier_part1 --output data\output\markiplier_part1_validation.txt --model data\models\1\model.pt --labels data\labels\markiplier_part1.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\markiplier_part2 --output data\output\markiplier_part2_validation.txt --model data\models\1\model.pt --labels data\labels\markiplier_part2.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\logan_paul --output data\output\logan_paul_validation.txt --model data\models\1\model.pt --labels data\labels\logan_paul.json

echo model v2
python scripts\analyze_emotions_with_validation.py --input data\video_frames\penguinz0 --output data\output\penguinz0_validation.txt --model data\models\2\model.pt --labels data\labels\penguinz0.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\michael_reeves --output data\output\michael_reeves_validation.txt --model data\models\2\model.pt --labels data\labels\michael_reeves.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\tommyinnit --output data\output\tommyinnit_validation.txt --model data\models\2\model.pt --labels data\labels\tommyinnit.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\mrballen --output data\output\mrballen_validation.txt --model data\models\2\model.pt --labels data\labels\mrballen.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\markiplier_part1 --output data\output\markiplier_part1_validation.txt --model data\models\2\model.pt --labels data\labels\markiplier_part1.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\markiplier_part2 --output data\output\markiplier_part2_validation.txt --model data\models\2\model.pt --labels data\labels\markiplier_part2.json
python scripts\analyze_emotions_with_validation.py --input data\video_frames\logan_paul --output data\output\logan_paul_validation.txt --model data\models\2\model.pt --labels data\labels\logan_paul.json