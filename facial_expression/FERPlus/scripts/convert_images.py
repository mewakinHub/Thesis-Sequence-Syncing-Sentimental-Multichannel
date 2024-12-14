import os
from PIL import Image

# Paths for input and output folders
input_folder = "data/jaffe/"  # Path to your folder with .tiff images
output_folder = "data/jaffe_converted/"  # Path where converted .jpg images will be saved

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Convert each .tiff file to .jpg
for file_name in os.listdir(input_folder):
    if file_name.endswith(".tiff"):  # Check for .tiff files
        img_path = os.path.join(input_folder, file_name)
        img = Image.open(img_path)
        # Convert the image to RGB mode (required for JPEG format)
        img = img.convert("RGB")
        # Save the converted image as .jpg
        img.save(os.path.join(output_folder, file_name.replace(".tiff", ".jpg")), "JPEG")

print(f"Images converted and saved to {output_folder}")
